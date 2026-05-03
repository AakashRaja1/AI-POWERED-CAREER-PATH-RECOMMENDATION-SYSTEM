"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the video training part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import csv
import json
import math
import pickle
import random
import warnings
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
import torch
import yaml
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision import models

try:
    import imageio.v3 as iio
except Exception:  # pragma: no cover - optional dependency
    iio = None

try:
    from .config import TRAIT_ORDER
except ImportError:
    from config import TRAIT_ORDER


PIPELINE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = PIPELINE_DIR.parent
DEFAULT_DATASET_ROOT = BACKEND_DIR / "ml_personality" / "first-impressions"
DEFAULT_TRAIN_DIR = DEFAULT_DATASET_ROOT / "train"
DEFAULT_ANNOTATION_PATH = DEFAULT_DATASET_ROOT / "annotations" / "train-annotation" / "annotation_training.pkl"
DEFAULT_ARTIFACT_ROOT = PIPELINE_DIR / "artifacts" / "video_v2"
DEFAULT_MODEL_DIR = PIPELINE_DIR / "models"
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


@dataclass(frozen=True)
class VideoTrainingConfig:
    use_subset: bool = True
    subset_size: int = 1000
    random_seed: int = 42
    frames_per_video: int = 12
    img_size: int = 224
    train_split: float = 0.7
    val_split: float = 0.15
    test_split: float = 0.15
    backbone: str = "resnet50"
    batch_size: int = 16
    epochs: int = 10
    lr: float = 1e-4
    dropout: float = 0.4
    weight_decay: float = 1e-4
    early_stopping_patience: int = 3
    reduce_lr_patience: int = 2
    temperature_scaling: bool = True
    debug: bool = False
    debug_sample_predictions: int = 5
    save_debug_frames: bool = False
    dataset_root: Path = DEFAULT_DATASET_ROOT
    train_dir: Path = DEFAULT_TRAIN_DIR
    annotation_path: Path = DEFAULT_ANNOTATION_PATH
    artifact_root: Path = DEFAULT_ARTIFACT_ROOT
    model_dir: Path = DEFAULT_MODEL_DIR
    model_v2_path: Path = DEFAULT_MODEL_DIR / "model_v2_best.pth"
    run_config_snapshot_path: Path = DEFAULT_ARTIFACT_ROOT / "run_config_snapshot.yaml"
    data_index_path: Path = DEFAULT_ARTIFACT_ROOT / "data_index.csv"
    selected_videos_path: Path = DEFAULT_ARTIFACT_ROOT / "selected_videos.csv"
    labels_path: Path = DEFAULT_ARTIFACT_ROOT / "labels.csv"
    labels_schema_path: Path = DEFAULT_ARTIFACT_ROOT / "labels_schema.json"
    train_split_path: Path = DEFAULT_ARTIFACT_ROOT / "train.csv"
    val_split_path: Path = DEFAULT_ARTIFACT_ROOT / "val.csv"
    test_split_path: Path = DEFAULT_ARTIFACT_ROOT / "test.csv"
    metrics_path: Path = DEFAULT_ARTIFACT_ROOT / "metrics.json"
    training_curves_path: Path = DEFAULT_ARTIFACT_ROOT / "training_curves.png"
    confusion_matrix_path: Path = DEFAULT_ARTIFACT_ROOT / "confusion_matrix.png"
    confidence_histogram_path: Path = DEFAULT_ARTIFACT_ROOT / "confidence_histogram.png"
    test_predictions_path: Path = DEFAULT_ARTIFACT_ROOT / "test_predictions.csv"
    plot_padding: int = 36
    trait_order: tuple[str, ...] = field(default_factory=lambda: tuple(TRAIT_ORDER))
    artifact_subdir: str = "video_v2"


@dataclass(frozen=True)
class VideoRecord:
    video_id: str
    video_path: Path


@dataclass(frozen=True)
class SplitRecord:
    video_id: str
    video_path: Path
    labels: dict[str, float]


def load_yaml_config(config_path: Path) -> dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Config file must contain a mapping: {config_path}")
    return payload


def _resolve_path(base_dir: Path, value: str | Path | None) -> Path:
    if value is None:
        return base_dir
    path = Path(value)
    return path if path.is_absolute() else (base_dir / path).resolve()


def build_config(config_path: Path) -> VideoTrainingConfig:
    raw = load_yaml_config(config_path)
    pipeline_dir = PIPELINE_DIR
    dataset_root = _resolve_path(pipeline_dir, raw.get("dataset_root", DEFAULT_DATASET_ROOT))
    train_dir = _resolve_path(pipeline_dir, raw.get("train_dir", dataset_root / "train"))
    annotation_path = _resolve_path(
        pipeline_dir,
        raw.get("annotation_path", dataset_root / "annotations" / "train-annotation" / "annotation_training.pkl"),
    )
    artifact_root = _resolve_path(pipeline_dir, raw.get("artifact_root", DEFAULT_ARTIFACT_ROOT))
    model_dir = _resolve_path(pipeline_dir, raw.get("model_dir", DEFAULT_MODEL_DIR))
    return replace(
        VideoTrainingConfig(),
        use_subset=bool(raw.get("use_subset", True)),
        subset_size=int(raw.get("subset_size", 1000)),
        random_seed=int(raw.get("random_seed", 42)),
        frames_per_video=int(raw.get("frames_per_video", 12)),
        img_size=int(raw.get("img_size", 224)),
        train_split=float(raw.get("train_split", 0.7)),
        val_split=float(raw.get("val_split", 0.15)),
        test_split=float(raw.get("test_split", 0.15)),
        backbone=str(raw.get("backbone", "resnet50")),
        batch_size=int(raw.get("batch_size", 16)),
        epochs=int(raw.get("epochs", 10)),
        lr=float(raw.get("lr", 1e-4)),
        dropout=float(raw.get("dropout", 0.4)),
        dataset_root=dataset_root,
        train_dir=train_dir,
        annotation_path=annotation_path,
        artifact_root=artifact_root,
        model_dir=model_dir,
        model_v2_path=model_dir / "model_v2_best.pth",
        run_config_snapshot_path=artifact_root / "run_config_snapshot.yaml",
        data_index_path=artifact_root / "data_index.csv",
        selected_videos_path=artifact_root / "selected_videos.csv",
        labels_path=artifact_root / "labels.csv",
        labels_schema_path=artifact_root / "labels_schema.json",
        train_split_path=artifact_root / "train.csv",
        val_split_path=artifact_root / "val.csv",
        test_split_path=artifact_root / "test.csv",
        metrics_path=artifact_root / "metrics.json",
        training_curves_path=artifact_root / "training_curves.png",
        confusion_matrix_path=artifact_root / "confusion_matrix.png",
        confidence_histogram_path=artifact_root / "confidence_histogram.png",
        test_predictions_path=artifact_root / "test_predictions.csv",
    )


def ensure_parent(path: Path | str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def normalize_video_id(value: str | Path) -> str:
    return Path(str(value)).stem


def read_annotation_mapping(annotation_path: Path) -> dict[str, dict[str, float]]:
    if not annotation_path.exists():
        raise FileNotFoundError(f"Annotation file not found: {annotation_path}")

    if annotation_path.suffix.lower() == ".zip":
        import zipfile

        with zipfile.ZipFile(annotation_path, "r") as archive:
            name = next((member for member in archive.namelist() if member.endswith(".pkl")), None)
            if name is None:
                raise ValueError(f"No pickle file found inside {annotation_path}")
            with archive.open(name, "r") as handle:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    payload = pickle.load(handle, encoding="latin1")
    else:
        with open(annotation_path, "rb") as handle:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                payload = pickle.load(handle, encoding="latin1")

    if not isinstance(payload, dict):
        raise ValueError("Annotation payload must be a mapping of trait -> labels")

    trait_maps: dict[str, dict[str, float]] = {}
    for trait_name, mapping in payload.items():
        if isinstance(mapping, dict):
            trait_maps[str(trait_name)] = {normalize_video_id(file_name): float(score) for file_name, score in mapping.items()}
    return trait_maps


def build_master_index(train_dir: Path) -> list[VideoRecord]:
    if not train_dir.exists():
        raise FileNotFoundError(f"Video directory not found: {train_dir}")

    records = [VideoRecord(video_id=path.stem, video_path=path) for path in sorted(train_dir.iterdir()) if path.suffix.lower() in VIDEO_EXTENSIONS]
    if not records:
        raise ValueError(f"No video files found in {train_dir}")
    return records


def select_subset(records: Sequence[VideoRecord], use_subset: bool, subset_size: int, seed: int) -> list[VideoRecord]:
    record_list = list(records)
    rng = random.Random(seed)
    rng.shuffle(record_list)
    if use_subset:
        return record_list[: min(subset_size, len(record_list))]
    return record_list


def build_labels(records: Sequence[VideoRecord], trait_maps: dict[str, dict[str, float]], trait_order: Sequence[str]) -> list[dict[str, Any]]:
    normalized_trait_maps = {trait: trait_maps[trait] for trait in trait_order if trait in trait_maps}
    missing_traits = [trait for trait in trait_order if trait not in normalized_trait_maps]
    if missing_traits:
        raise ValueError(f"Missing traits in annotation file: {missing_traits}")

    rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for record in records:
        if any(record.video_id not in normalized_trait_maps[trait] for trait in trait_order):
            missing.append(record.video_id)
            continue
        row = {"video_id": record.video_id}
        row.update({trait: float(normalized_trait_maps[trait][record.video_id]) for trait in trait_order})
        rows.append(row)

    if missing:
        preview = ", ".join(missing[:10])
        raise ValueError(f"Missing labels for {len(missing)} videos. Examples: {preview}")
    return rows


def write_csv(path: Path, rows: Sequence[dict[str, Any]], fieldnames: Sequence[str]) -> None:
    ensure_parent(path)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


def write_data_index(path: Path, records: Sequence[VideoRecord], dataset_root: Path) -> None:
    rows = [
        {
            "video_id": record.video_id,
            "video_path": record.video_path.relative_to(dataset_root).as_posix(),
        }
        for record in records
    ]
    write_csv(path, rows, ["video_id", "video_path"])


def write_labels(path: Path, rows: Sequence[dict[str, Any]], trait_order: Sequence[str]) -> None:
    write_csv(path, rows, ["video_id", *trait_order])


def split_records(records: Sequence[VideoRecord], train_split: float, val_split: float, test_split: float, seed: int) -> tuple[list[VideoRecord], list[VideoRecord], list[VideoRecord]]:
    if not math.isclose(train_split + val_split + test_split, 1.0, abs_tol=1e-6):
        raise ValueError("train_split + val_split + test_split must equal 1.0")

    shuffled = list(records)
    random.Random(seed).shuffle(shuffled)
    total = len(shuffled)
    train_count = int(total * train_split)
    val_count = int(total * val_split)
    test_count = total - train_count - val_count
    if test_count < 0:
        raise ValueError("Split ratios produce a negative test split")

    train_records = shuffled[:train_count]
    val_records = shuffled[train_count : train_count + val_count]
    test_records = shuffled[train_count + val_count :]
    return train_records, val_records, test_records


def assert_split_safety(train_records: Sequence[VideoRecord], val_records: Sequence[VideoRecord], test_records: Sequence[VideoRecord]) -> None:
    train_ids = {record.video_id for record in train_records}
    val_ids = {record.video_id for record in val_records}
    test_ids = {record.video_id for record in test_records}
    if train_ids & val_ids or train_ids & test_ids or val_ids & test_ids:
        raise AssertionError("Video leakage detected across splits")
    if len(train_ids) + len(val_ids) + len(test_ids) != len(train_records) + len(val_records) + len(test_records):
        raise AssertionError("Split counts do not match the number of records")


def combine_split_rows(records: Sequence[VideoRecord], labels_lookup: dict[str, dict[str, float]], trait_order: Sequence[str], dataset_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        row = {
            "video_id": record.video_id,
            "video_path": record.video_path.relative_to(dataset_root).as_posix(),
        }
        row.update({trait: float(labels_lookup[trait][record.video_id]) for trait in trait_order})
        rows.append(row)
    return rows


def build_labels_schema(trait_order: Sequence[str]) -> dict[str, Any]:
    trait_descriptions = {
        "openness": "Openness to new experience, curiosity, imagination, and intellectual flexibility.",
        "conscientiousness": "Organization, dependability, discipline, and goal-directed behavior.",
        "extraversion": "Sociability, assertiveness, energy, and expressive engagement.",
        "agreeableness": "Warmth, cooperation, empathy, and interpersonal trust.",
        "neuroticism": "Emotional instability, stress sensitivity, and negative affect.",
    }
    trait_directions = {
        trait: "Higher values indicate a stronger presence of this trait." for trait in trait_order
    }
    return {
        "label_type": "continuous_regression",
        "value_range": [0.0, 1.0],
        "trait_order": list(trait_order),
        "traits": {
            trait: {
                "description": trait_descriptions.get(trait, trait),
                "higher_is": trait_directions.get(trait, "Higher values indicate a stronger presence of this trait."),
            }
            for trait in trait_order
        },
    }


def save_labels_schema(path: Path, trait_order: Sequence[str]) -> None:
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(build_labels_schema(trait_order), handle, indent=2)


def _frame_transform(training: bool, img_size: int) -> transforms.Compose:
    steps: list[Any] = [transforms.Resize((img_size, img_size))]
    if training:
        steps.append(transforms.RandomHorizontalFlip(p=0.5))
    steps.extend(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ]
    )
    return transforms.Compose(steps)


def _load_frame_from_path(file_path: Path) -> Image.Image:
    try:
        return Image.open(file_path).convert("RGB")
    except (FileNotFoundError, OSError, UnidentifiedImageError) as error:
        raise RuntimeError(f"Unable to load frame from {file_path}: {error}") from error


def _sample_frame_indices(frame_count: int, frames_per_video: int) -> list[int]:
    if frame_count <= 0:
        return [0] * frames_per_video
    positions = np.linspace(0, frame_count - 1, frames_per_video)
    return [int(round(value)) for value in positions]


def load_video_frames(video_path: Path, frames_per_video: int) -> list[Image.Image]:
    if iio is None:
        raise RuntimeError("Reading video files requires imageio. Install the pipeline requirements first.")

    frames_per_video = max(1, int(frames_per_video))
    frame_indices: list[int] = []
    try:
        properties = iio.improps(str(video_path))
        total_frames = int(getattr(properties, "n_images", 0) or 0)
        if total_frames > 0:
            frame_indices = _sample_frame_indices(total_frames, frames_per_video)
    except Exception:
        frame_indices = []

    frames: list[Image.Image] = []
    if frame_indices:
        for frame_index in frame_indices:
            try:
                frame = iio.imread(str(video_path), index=frame_index)
                frames.append(Image.fromarray(frame).convert("RGB"))
            except Exception:
                continue

    if not frames:
        try:
            iterator = iio.imiter(str(video_path))
            buffered = []
            for frame in iterator:
                buffered.append(Image.fromarray(frame).convert("RGB"))
            if buffered:
                frame_indices = _sample_frame_indices(len(buffered), frames_per_video)
                frames = [buffered[index] for index in frame_indices]
        except Exception as error:
            raise RuntimeError(f"Failed to read video {video_path}: {error}") from error

    if not frames:
        raise RuntimeError(f"Could not decode any frame from {video_path}")

    if len(frames) < frames_per_video:
        frames = frames + [frames[-1]] * (frames_per_video - len(frames))

    return frames[:frames_per_video]


class VideoDataset(Dataset):
    def __init__(self, rows: Sequence[dict[str, Any]], trait_order: Sequence[str], frames_per_video: int, img_size: int, training: bool = False) -> None:
        self.rows = list(rows)
        self.trait_order = list(trait_order)
        self.frames_per_video = int(frames_per_video)
        self.transform = _frame_transform(training=training, img_size=img_size)

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int):
        row = self.rows[index]
        video_path = Path(row["video_path"])
        if not video_path.is_absolute():
            video_path = DEFAULT_DATASET_ROOT / video_path
        frames = [self.transform(frame) for frame in load_video_frames(video_path, self.frames_per_video)]
        target = torch.tensor([float(row[trait]) for trait in self.trait_order], dtype=torch.float32)
        stacked = torch.stack(frames, dim=0)
        return stacked, target, row["video_id"], str(video_path)


def _get_backbone(backbone_name: str) -> tuple[nn.Module, int]:
    backbone_name = backbone_name.lower().strip()
    if backbone_name == "resnet50":
        weights = None
        try:
            weights = models.ResNet50_Weights.DEFAULT
        except Exception:
            weights = None
        model = models.resnet50(weights=weights)
        feature_dim = model.fc.in_features
        model.fc = nn.Identity()
        return model, feature_dim

    if backbone_name == "efficientnet_b0":
        weights = None
        try:
            weights = models.EfficientNet_B0_Weights.DEFAULT
        except Exception:
            weights = None
        model = models.efficientnet_b0(weights=weights)
        feature_dim = model.classifier[1].in_features
        model.classifier = nn.Identity()
        return model, feature_dim

    raise ValueError("backbone must be either 'resnet50' or 'efficientnet_b0'")


class VideoRegressionModel(nn.Module):
    def __init__(self, backbone_name: str, output_dim: int, dropout: float) -> None:
        super().__init__()
        backbone, feature_dim = _get_backbone(backbone_name)
        for parameter in backbone.parameters():
            parameter.requires_grad = False
        backbone.eval()
        self.backbone = backbone
        self.feature_dim = feature_dim
        self.head = nn.Sequential(
            nn.Linear(feature_dim, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(512, output_dim),
        )

    def forward(self, video_frames: torch.Tensor) -> torch.Tensor:
        batch_size, frames_per_video, channels, height, width = video_frames.shape
        flat = video_frames.reshape(batch_size * frames_per_video, channels, height, width)
        features = self.backbone(flat)
        if features.ndim > 2:
            features = torch.flatten(features, start_dim=1)
        features = features.reshape(batch_size, frames_per_video, -1)
        pooled = features.mean(dim=1)
        return self.head(pooled)


def build_dataloader(rows: Sequence[dict[str, Any]], trait_order: Sequence[str], config: VideoTrainingConfig, training: bool) -> DataLoader:
    dataset = VideoDataset(rows, trait_order, frames_per_video=config.frames_per_video, img_size=config.img_size, training=training)
    generator = torch.Generator()
    generator.manual_seed(config.random_seed)
    return DataLoader(
        dataset,
        batch_size=config.batch_size,
        shuffle=training,
        num_workers=0,
        pin_memory=False,
        generator=generator if training else None,
    )


def infer_label_mode(rows: Sequence[dict[str, Any]], trait_order: Sequence[str]) -> str:
    values = [float(row[trait]) for row in rows for trait in trait_order]
    if all(abs(value - round(value)) < 1e-8 for value in values):
        return "binary"
    return "regression"


def _loss_fn(label_mode: str):
    if label_mode == "binary":
        return nn.BCEWithLogitsLoss()
    return nn.MSELoss()


def _probabilities_from_logits(logits: torch.Tensor, temperature: float) -> torch.Tensor:
    temperature = max(float(temperature), 1e-6)
    return torch.sigmoid(logits / temperature)


def evaluate_loader(model: nn.Module, loader: DataLoader, trait_order: Sequence[str], label_mode: str, temperature: float = 1.0) -> dict[str, Any]:
    model.eval()
    batch_logits: list[torch.Tensor] = []
    batch_targets: list[torch.Tensor] = []
    batch_video_ids: list[str] = []
    batch_video_paths: list[str] = []

    with torch.no_grad():
        for frames, targets, video_ids, video_paths in loader:
            logits = model(frames)
            batch_logits.append(logits.cpu())
            batch_targets.append(targets.cpu())
            batch_video_ids.extend(list(video_ids))
            batch_video_paths.extend(list(video_paths))

    if not batch_logits:
        raise ValueError("Loader produced no batches")

    logits = torch.cat(batch_logits, dim=0)
    targets = torch.cat(batch_targets, dim=0)
    probabilities = _probabilities_from_logits(logits, temperature)
    predictions = (probabilities >= 0.5).int()
    truths = (targets >= 0.5).int()

    per_trait: dict[str, dict[str, float]] = {}
    confusion_payload: dict[str, list[list[int]]] = {}
    for index, trait in enumerate(trait_order):
        trait_true = truths[:, index].numpy()
        trait_pred = predictions[:, index].numpy()
        precision, recall, f1, _ = precision_recall_fscore_support(
            trait_true,
            trait_pred,
            average="binary",
            zero_division=0,
        )
        cm = confusion_matrix(trait_true, trait_pred, labels=[0, 1]).tolist()
        per_trait[trait] = {
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
        }
        confusion_payload[trait] = [[int(value) for value in row] for row in cm]

    flat_true = truths.reshape(-1).numpy()
    flat_pred = predictions.reshape(-1).numpy()
    macro = precision_recall_fscore_support(flat_true, flat_pred, average="macro", zero_division=0)
    micro = precision_recall_fscore_support(flat_true, flat_pred, average="micro", zero_division=0)

    raw_rows: list[dict[str, Any]] = []
    confidence_values: list[float] = []
    for row_index, video_id in enumerate(batch_video_ids):
        row = {
            "video_id": video_id,
            "video_path": batch_video_paths[row_index],
        }
        confidence_values.append(float(probabilities[row_index].mean().item()))
        for trait_index, trait in enumerate(trait_order):
            row[f"logit_{trait}"] = float(logits[row_index, trait_index].item())
            row[f"prob_{trait}"] = float(probabilities[row_index, trait_index].item())
            row[f"target_{trait}"] = float(targets[row_index, trait_index].item())
            row[f"pred_{trait}"] = int(predictions[row_index, trait_index].item())
        row["confidence"] = float(probabilities[row_index].mean().item())
        raw_rows.append(row)

    return {
        "logits": logits,
        "targets": targets,
        "probabilities": probabilities,
        "predictions": predictions,
        "per_trait": per_trait,
        "confusion_payload": confusion_payload,
        "macro": {"precision": float(macro[0]), "recall": float(macro[1]), "f1": float(macro[2])},
        "micro": {"precision": float(micro[0]), "recall": float(micro[1]), "f1": float(micro[2])},
        "raw_rows": raw_rows,
        "confidence_values": confidence_values,
    }


def fit_temperature(logits: torch.Tensor, targets: torch.Tensor, label_mode: str) -> float:
    if label_mode == "binary":
        criterion = nn.BCEWithLogitsLoss()
    else:
        criterion = nn.MSELoss()

    temperature = torch.tensor([1.0], requires_grad=True)
    optimizer = torch.optim.LBFGS([temperature], lr=0.05, max_iter=50, line_search_fn="strong_wolfe")

    def closure():
        optimizer.zero_grad()
        scaled = torch.sigmoid(logits / temperature.clamp(min=1e-3))
        if label_mode == "binary":
            loss = criterion(logits / temperature.clamp(min=1e-3), targets)
        else:
            loss = criterion(scaled, targets)
        loss.backward()
        return loss

    try:
        optimizer.step(closure)
    except Exception:
        return 1.0

    return float(temperature.detach().clamp(min=1e-3).item())


def save_checkpoint(path: Path, model: nn.Module, config: VideoTrainingConfig, trait_order: Sequence[str], label_mode: str, metadata: dict[str, Any]) -> None:
    ensure_parent(path)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "metadata": metadata,
            "trait_order": list(trait_order),
            "label_mode": label_mode,
            "config": {key: str(value) if isinstance(value, Path) else value for key, value in asdict(config).items()},
        },
        path,
    )


def _load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size=size)
    except Exception:
        return ImageFont.load_default()


def draw_line_plot(path: Path, history: Sequence[dict[str, float]]) -> None:
    width, height = 1200, 720
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = _load_font(18)
    title_font = _load_font(24)

    margin = 70
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    draw.text((margin, 20), "Training Curves", fill="black", font=title_font)
    draw.rectangle([margin, margin, width - margin, height - margin], outline="black", width=2)

    if not history:
        image.save(path)
        return

    epochs = [row["epoch"] for row in history]
    train_losses = [row["train_loss"] for row in history]
    val_losses = [row["val_loss"] for row in history]
    train_f1 = [row.get("train_f1") for row in history if "train_f1" in row]
    val_f1 = [row["val_f1"] for row in history if "val_f1" in row]
    max_loss = max(train_losses + val_losses + [1e-6])

    def point(index: int, values: Sequence[float]) -> tuple[int, int]:
        if len(values) == 1:
            x = margin + plot_width // 2
        else:
            x = margin + int(plot_width * index / (len(values) - 1))
        y = margin + int(plot_height * (1.0 - min(1.0, values[index] / max_loss)))
        return x, y

    loss_points_train = [point(index, train_losses) for index in range(len(train_losses))]
    loss_points_val = [point(index, val_losses) for index in range(len(val_losses))]

    for points, color in ((loss_points_train, "#1f77b4"), (loss_points_val, "#d62728")):
        if len(points) > 1:
            draw.line(points, fill=color, width=4)
        for point_xy in points:
            draw.ellipse([point_xy[0] - 4, point_xy[1] - 4, point_xy[0] + 4, point_xy[1] + 4], fill=color)

    f1_scale_y = height - margin - 20
    if train_f1:
        for index, value in enumerate(train_f1):
            x = margin + int(plot_width * index / max(1, len(train_f1) - 1))
            y = f1_scale_y - int((plot_height - 120) * value)
            draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill="#2ca02c")
    if val_f1:
        for index, value in enumerate(val_f1):
            x = margin + int(plot_width * index / max(1, len(val_f1) - 1))
            y = f1_scale_y - int((plot_height - 120) * value)
            draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill="#ff7f0e")

    draw.text((margin + 10, margin + 10), "Loss: blue=train, red=val", fill="black", font=font)
    draw.text((margin + 10, margin + 35), "F1 markers: green=train, orange=val", fill="black", font=font)
    draw.text((margin + 10, height - margin + 8), f"Epochs: {len(history)}", fill="black", font=font)
    image.save(path)


def draw_confusion_grid(path: Path, trait_order: Sequence[str], confusion_payload: dict[str, list[list[int]]]) -> None:
    columns = 2
    rows = math.ceil(len(trait_order) / columns)
    cell_size = 320
    width = columns * cell_size
    height = rows * cell_size
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = _load_font(18)
    title_font = _load_font(22)

    for index, trait in enumerate(trait_order):
        row_index = index // columns
        col_index = index % columns
        left = col_index * cell_size + 20
        top = row_index * cell_size + 20
        draw.text((left, top), trait, fill="black", font=title_font)
        matrix = confusion_payload.get(trait, [[0, 0], [0, 0]])
        max_value = max(1, max(max(row) for row in matrix))
        for y_index, row_values in enumerate(matrix):
            for x_index, value in enumerate(row_values):
                intensity = int(255 - 160 * (value / max_value))
                color = (255, intensity, intensity)
                x0 = left + x_index * 110
                y0 = top + 60 + y_index * 110
                draw.rectangle([x0, y0, x0 + 100, y0 + 100], fill=color, outline="black", width=2)
                draw.text((x0 + 30, y0 + 36), str(int(value)), fill="black", font=font)

    image.save(path)


def draw_histogram(path: Path, confidence_values: Sequence[float]) -> None:
    width, height = 1000, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = _load_font(18)
    title_font = _load_font(24)
    draw.text((30, 20), "Confidence Distribution", fill="black", font=title_font)

    bins = np.linspace(0.0, 1.0, 11)
    counts, _ = np.histogram(np.asarray(confidence_values, dtype=np.float32), bins=bins)
    max_count = max(1, int(counts.max()))
    margin = 70
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    bar_width = plot_width // len(counts)
    for index, count in enumerate(counts):
        bar_height = int(plot_height * (count / max_count))
        x0 = margin + index * bar_width + 6
        y0 = height - margin - bar_height
        draw.rectangle([x0, y0, x0 + bar_width - 12, height - margin], fill="#1f77b4", outline="black")
        draw.text((x0 + 8, y0 - 18), str(int(count)), fill="black", font=font)

    image.save(path)


def save_predictions_csv(path: Path, rows: Sequence[dict[str, Any]], trait_order: Sequence[str]) -> None:
    fieldnames = ["video_id", "video_path", *[f"logit_{trait}" for trait in trait_order], *[f"prob_{trait}" for trait in trait_order], *[f"target_{trait}" for trait in trait_order], *[f"pred_{trait}" for trait in trait_order], "confidence"]
    write_csv(path, rows, fieldnames)


def save_metrics(path: Path, payload: dict[str, Any]) -> None:
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def train_video_model(config: VideoTrainingConfig) -> dict[str, Any]:
    seed_everything(config.random_seed)
    config.artifact_root.mkdir(parents=True, exist_ok=True)
    config.model_dir.mkdir(parents=True, exist_ok=True)

    master_index = build_master_index(config.train_dir)
    write_data_index(config.data_index_path, master_index, config.dataset_root)

    selected_records = select_subset(master_index, config.use_subset, config.subset_size, config.random_seed)
    write_data_index(config.selected_videos_path, selected_records, config.dataset_root)

    trait_maps = read_annotation_mapping(config.annotation_path)
    labels_rows = build_labels(selected_records, trait_maps, config.trait_order)
    write_labels(config.labels_path, labels_rows, config.trait_order)
    save_labels_schema(config.labels_schema_path, config.trait_order)

    labels_lookup = {trait: trait_maps[trait] for trait in config.trait_order}
    train_records, val_records, test_records = split_records(selected_records, config.train_split, config.val_split, config.test_split, config.random_seed)
    assert_split_safety(train_records, val_records, test_records)

    train_rows = combine_split_rows(train_records, labels_lookup, config.trait_order, config.dataset_root)
    val_rows = combine_split_rows(val_records, labels_lookup, config.trait_order, config.dataset_root)
    test_rows = combine_split_rows(test_records, labels_lookup, config.trait_order, config.dataset_root)
    write_csv(config.train_split_path, train_rows, ["video_id", "video_path", *config.trait_order])
    write_csv(config.val_split_path, val_rows, ["video_id", "video_path", *config.trait_order])
    write_csv(config.test_split_path, test_rows, ["video_id", "video_path", *config.trait_order])

    label_mode = infer_label_mode(labels_rows, config.trait_order)
    model = VideoRegressionModel(config.backbone, output_dim=len(config.trait_order), dropout=config.dropout)
    train_loader = build_dataloader(train_rows, config.trait_order, config, training=True)
    val_loader = build_dataloader(val_rows, config.trait_order, config, training=False)
    test_loader = build_dataloader(test_rows, config.trait_order, config, training=False)

    optimizer = torch.optim.AdamW((parameter for parameter in model.parameters() if parameter.requires_grad), lr=config.lr, weight_decay=config.weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", patience=config.reduce_lr_patience, factor=0.5)
    criterion = _loss_fn(label_mode)

    best_val_loss = math.inf
    best_temperature = 1.0
    epochs_without_improvement = 0
    history: list[dict[str, float]] = []
    best_state: dict[str, Any] | None = None

    for epoch in range(1, config.epochs + 1):
        model.train()
        train_loss_total = 0.0
        train_items = 0

        for frames, targets, _, _ in train_loader:
            optimizer.zero_grad(set_to_none=True)
            logits = model(frames)
            loss = criterion(logits, targets) if label_mode == "binary" else criterion(torch.sigmoid(logits), targets)
            loss.backward()
            optimizer.step()
            train_loss_total += float(loss.item()) * frames.size(0)
            train_items += frames.size(0)

        val_eval = evaluate_loader(model, val_loader, config.trait_order, label_mode, temperature=1.0)
        train_loss = train_loss_total / max(1, train_items)
        val_loss = float(nn.functional.mse_loss(val_eval["probabilities"], val_eval["targets"]).item()) if label_mode != "binary" else float(nn.functional.binary_cross_entropy_with_logits(val_eval["logits"], val_eval["targets"]).item())
        scheduler.step(val_loss)
        history.append(
            {
                "epoch": float(epoch),
                "train_loss": train_loss,
                "val_loss": val_loss,
                "val_f1": val_eval["macro"]["f1"],
            }
        )

        print(f"Epoch {epoch}/{config.epochs} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_f1={val_eval['macro']['f1']:.4f}", flush=True)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_without_improvement = 0
            if config.temperature_scaling:
                best_temperature = fit_temperature(val_eval["logits"], val_eval["targets"], label_mode)
            best_state = {
                "model_state_dict": model.state_dict(),
                "metadata": {
                    "architecture": "cnn_mean_pool_v2",
                    "backbone": config.backbone,
                    "frames_per_video": config.frames_per_video,
                    "img_size": config.img_size,
                    "label_mode": label_mode,
                    "train_count": len(train_rows),
                    "val_count": len(val_rows),
                    "test_count": len(test_rows),
                    "selected_count": len(selected_records),
                    "best_val_loss": best_val_loss,
                    "temperature": best_temperature,
                    "trait_order": list(config.trait_order),
                    "dropout": config.dropout,
                },
            }
            save_checkpoint(config.model_v2_path, model, config, config.trait_order, label_mode, best_state["metadata"])
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= config.early_stopping_patience:
                print("Early stopping triggered.")
                break

    draw_line_plot(config.training_curves_path, history)

    if best_state is None:
        checkpoint = torch.load(config.model_v2_path, map_location="cpu")
        best_temperature = float(checkpoint.get("metadata", {}).get("temperature", 1.0))
        best_state = checkpoint

    checkpoint = torch.load(config.model_v2_path, map_location="cpu")
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    test_eval = evaluate_loader(model, test_loader, config.trait_order, label_mode, temperature=best_temperature)
    if test_eval["macro"]["f1"] == 1.0 or test_eval["micro"]["f1"] == 1.0:
        warnings.warn("Possible data leakage or evaluation bug", RuntimeWarning)

    save_predictions_csv(config.test_predictions_path, test_eval["raw_rows"], config.trait_order)
    draw_confusion_grid(config.confusion_matrix_path, config.trait_order, test_eval["confusion_payload"])
    draw_histogram(config.confidence_histogram_path, test_eval["confidence_values"])

    metrics_payload = {
        "summary": {
            "label_mode": label_mode,
            "backbone": config.backbone,
            "subset_used": config.use_subset,
            "subset_size": len(selected_records),
            "train_count": len(train_rows),
            "val_count": len(val_rows),
            "test_count": len(test_rows),
            "temperature": best_temperature,
            "best_model_path": str(config.model_v2_path),
            "seed": config.random_seed,
        },
        "macro": test_eval["macro"],
        "micro": test_eval["micro"],
        "per_trait": test_eval["per_trait"],
        "confusion_matrix": test_eval["confusion_payload"],
        "best_val_loss": best_val_loss,
        "history": history,
    }
    save_metrics(config.metrics_path, metrics_payload)

    config_snapshot = {key: str(value) if isinstance(value, Path) else value for key, value in asdict(config).items()}
    config_snapshot["best_model_path"] = str(config.model_v2_path)
    config_snapshot["trait_order"] = list(config.trait_order)
    ensure_parent(config.run_config_snapshot_path)
    with open(config.run_config_snapshot_path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(config_snapshot, handle, sort_keys=False)

    if config.debug:
        print("Debug sample predictions")
        for index, row in enumerate(test_eval["raw_rows"][: config.debug_sample_predictions]):
            predicted = [round(float(row[f"prob_{trait}"]), 3) for trait in config.trait_order]
            actual = [round(float(row[f"target_{trait}"]), 3) for trait in config.trait_order]
            confidence = round(float(row["confidence"]), 3)
            print(f"{index + 1}. {row['video_id']} | pred={predicted} | gt={actual} | confidence={confidence}")

    return metrics_payload
