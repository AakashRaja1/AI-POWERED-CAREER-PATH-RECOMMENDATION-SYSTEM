"""
Dataset loading module for personality training. It reads labels and media paths, applies preprocessing, and returns examples in the shape expected by PyTorch.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import json
import pickle
import random
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

import torch
from PIL import Image
from torch.utils.data import Dataset

try:
    import imageio.v3 as iio
except Exception:  # pragma: no cover - optional dependency
    iio = None

try:
    from .config import TRAIT_ORDER
except ImportError:
    from config import TRAIT_ORDER


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


@dataclass(frozen=True)
class PersonalitySample:
    path: Path
    target: List[float]


def load_annotation_mapping(annotation_path: Path) -> Dict[str, Dict[str, float]]:
    if not annotation_path.exists():
        raise FileNotFoundError(f"Annotation file not found: {annotation_path}")

    if annotation_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(annotation_path, "r") as archive:
            pkl_name = next((name for name in archive.namelist() if name.endswith(".pkl")), None)
            if pkl_name is None:
                raise ValueError(f"No pickle file found inside {annotation_path}")
            with archive.open(pkl_name, "r") as handle:
                return pickle.load(handle, encoding="latin1")

    with open(annotation_path, "rb") as handle:
        return pickle.load(handle, encoding="latin1")


def load_extra_labels(extra_labels_path: Path) -> Dict[str, Dict[str, float]]:
    if not extra_labels_path.exists():
        raise FileNotFoundError(f"Extra labels file not found: {extra_labels_path}")

    with open(extra_labels_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError("Extra labels JSON must be a mapping of file_name -> trait dictionary")

    normalized: Dict[str, Dict[str, float]] = {}
    for file_name, trait_map in payload.items():
        if not isinstance(trait_map, Mapping):
            continue
        normalized[str(file_name)] = {str(name): float(value) for name, value in trait_map.items()}
    return normalized


def build_samples(
    split_dir: Path,
    annotation_path: Path,
    limit_ratio: float = 1.0,
    seed: int = 42,
    extra_labels: Mapping[str, Mapping[str, float]] | None = None,
    extra_trait_order: Sequence[str] = (),
) -> List[PersonalitySample]:
    if not split_dir.exists():
        raise FileNotFoundError(f"Split directory not found: {split_dir}")

    annotations = load_annotation_mapping(annotation_path)
    trait_maps = {trait: annotations[trait] for trait in TRAIT_ORDER if trait in annotations}
    extra_trait_order = tuple(str(name) for name in extra_trait_order)

    candidates: List[PersonalitySample] = []
    for file_path in sorted(split_dir.iterdir()):
        if file_path.suffix.lower() not in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
            continue

        key = file_path.name
        if any(key not in trait_map for trait_map in trait_maps.values()):
            continue

        target = [float(trait_maps[trait][key]) for trait in TRAIT_ORDER]

        if extra_trait_order:
            if extra_labels is None or key not in extra_labels:
                continue
            item_labels = extra_labels[key]
            if any(trait not in item_labels for trait in extra_trait_order):
                continue
            target.extend(float(item_labels[trait]) for trait in extra_trait_order)

        candidates.append(PersonalitySample(path=file_path, target=target))

    if not candidates:
        raise ValueError(f"No labeled samples found in {split_dir}")

    limit_ratio = float(limit_ratio)
    if 0 < limit_ratio < 1:
        random.Random(seed).shuffle(candidates)
        keep_count = max(1, int(len(candidates) * limit_ratio))
        candidates = candidates[:keep_count]

    return candidates


def _load_image(file_path: Path) -> Image.Image:
    return Image.open(file_path).convert("RGB")


def _load_video_frame(file_path: Path) -> Image.Image:
    if iio is None:
        raise RuntimeError(
            "Reading MP4 files requires imageio and imageio-ffmpeg. "
            "Install backend/ml_personality_pipeline/requirements.txt before training or inference."
        )

    try:
        frame = iio.imread(str(file_path), index=0)
    except TypeError:
        frame = next(iio.imiter(str(file_path)))
    except Exception as error:
        raise RuntimeError(f"Failed to read video {file_path}: {error}") from error

    return Image.fromarray(frame).convert("RGB")


def _load_video_frames(file_path: Path, max_frames: int = 1) -> List[Image.Image]:
    if iio is None:
        raise RuntimeError(
            "Reading MP4 files requires imageio and imageio-ffmpeg. "
            "Install backend/ml_personality_pipeline/requirements.txt before training or inference."
        )

    frame_count = max(1, int(max_frames))

    # Fast path: single representative frame.
    if frame_count == 1:
        return [_load_video_frame(file_path)]

    indices: List[int] = []
    try:
        props = iio.improps(str(file_path))
        n_images = int(getattr(props, "n_images", 0) or 0)
        if n_images > 0:
            indices = sorted(
                {
                    int(round(i * (n_images - 1) / max(1, frame_count - 1)))
                    for i in range(frame_count)
                }
            )
    except Exception:
        indices = []

    frames: List[Image.Image] = []
    if indices:
        for index in indices:
            try:
                frame = iio.imread(str(file_path), index=index)
                frames.append(Image.fromarray(frame).convert("RGB"))
            except Exception:
                continue

    # Fallback when metadata/random indexing is unavailable for a codec.
    if not frames:
        try:
            for idx, frame in enumerate(iio.imiter(str(file_path))):
                if idx >= frame_count:
                    break
                frames.append(Image.fromarray(frame).convert("RGB"))
        except Exception as error:
            raise RuntimeError(f"Failed to read video {file_path}: {error}") from error

    if not frames:
        raise RuntimeError(f"Could not decode any frame from {file_path}")

    return frames


def load_media(file_path: Path) -> Image.Image:
    suffix = file_path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return _load_image(file_path)
    if suffix in VIDEO_EXTENSIONS:
        return _load_video_frame(file_path)
    raise ValueError(f"Unsupported file type: {file_path}")


def load_media_frames(file_path: Path, max_frames: int = 1) -> List[Image.Image]:
    suffix = file_path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return [_load_image(file_path)]
    if suffix in VIDEO_EXTENSIONS:
        return _load_video_frames(file_path, max_frames=max_frames)
    raise ValueError(f"Unsupported file type: {file_path}")


class FirstImpressionsDataset(Dataset):
    def __init__(
        self,
        split_dir: Path,
        annotation_path: Path,
        transform=None,
        limit_ratio: float = 1.0,
        seed: int = 42,
        samples: List[PersonalitySample] | None = None,
        extra_labels: Mapping[str, Mapping[str, float]] | None = None,
        extra_trait_order: Sequence[str] = (),
    ) -> None:
        self.samples = samples if samples is not None else build_samples(
            split_dir,
            annotation_path,
            limit_ratio=limit_ratio,
            seed=seed,
            extra_labels=extra_labels,
            extra_trait_order=extra_trait_order,
        )
        self.transform = transform

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        sample = self.samples[index]
        image = load_media(sample.path)
        if self.transform is not None:
            image = self.transform(image)
        target = torch.tensor(sample.target, dtype=torch.float32)
        return image, target, sample.path.name
