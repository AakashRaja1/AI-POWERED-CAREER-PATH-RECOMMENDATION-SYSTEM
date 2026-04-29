from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageStat

try:
    from .config import DEFAULT_CONFIG, TRAIT_ORDER
    from .dataset_loader import build_samples, load_media
except ImportError:
    from config import DEFAULT_CONFIG, TRAIT_ORDER
    from dataset_loader import build_samples, load_media

try:
    import cv2
except Exception:  # pragma: no cover - optional local dependency
    cv2 = None


def _clamp(value: float, low: float = 0.05, high: float = 0.95) -> float:
    return max(low, min(high, float(value)))


def _normalize(values: list[float]) -> list[float]:
    lo = min(values)
    hi = max(values)
    span = hi - lo
    if span <= 1e-8:
        return [0.5 for _ in values]
    return [(value - lo) / span for value in values]


def _face_features(image: Image.Image) -> dict[str, float]:
    if cv2 is None:
        return {"face_size": 0.0, "face_center": 0.5}

    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(str(cascade_path))
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(24, 24))
    if len(faces) == 0:
        return {"face_size": 0.0, "face_center": 0.35}

    height, width = gray.shape[:2]
    x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
    face_size = (w * h) / max(1.0, width * height)
    center_x = (x + w / 2) / max(1.0, width)
    center_y = (y + h / 2) / max(1.0, height)
    center_distance = ((center_x - 0.5) ** 2 + (center_y - 0.45) ** 2) ** 0.5
    face_center = 1.0 - min(1.0, center_distance / 0.7)
    return {"face_size": face_size, "face_center": face_center}


def _raw_visual_features(image: Image.Image) -> dict[str, float]:
    rgb = image.convert("RGB")
    gray = image.convert("L")
    stat_rgb = ImageStat.Stat(rgb)
    stat_gray = ImageStat.Stat(gray)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_stat = ImageStat.Stat(edges)
    channels = np.array(rgb, dtype=np.float32) / 255.0

    features = {
        "brightness": stat_gray.mean[0] / 255.0,
        "contrast": stat_gray.stddev[0] / 128.0,
        "sharpness": edge_stat.mean[0] / 64.0,
        "saturation": float(np.mean(np.max(channels, axis=2) - np.min(channels, axis=2))),
        "color_balance": float(1.0 - min(1.0, np.std(stat_rgb.mean) / 80.0)),
    }
    features.update(_face_features(rgb))
    return features


def _pseudo_labels(feature_rows: list[dict[str, float]]) -> list[dict[str, float]]:
    names = ["brightness", "contrast", "sharpness", "saturation", "color_balance", "face_size", "face_center"]
    normalized = {
        name: _normalize([row[name] for row in feature_rows])
        for name in names
    }

    labels = []
    for index in range(len(feature_rows)):
        brightness = normalized["brightness"][index]
        contrast = normalized["contrast"][index]
        sharpness = normalized["sharpness"][index]
        saturation = normalized["saturation"][index]
        color_balance = normalized["color_balance"][index]
        face_size = normalized["face_size"][index]
        face_center = normalized["face_center"][index]
        darkness = 1.0 - brightness
        blur = 1.0 - sharpness
        off_center = 1.0 - face_center

        labels.append(
            {
                "openness": _clamp(0.25 + 0.28 * saturation + 0.22 * contrast + 0.20 * sharpness + 0.05 * brightness),
                "conscientiousness": _clamp(0.25 + 0.30 * sharpness + 0.25 * face_center + 0.15 * color_balance + 0.05 * brightness),
                "extraversion": _clamp(0.25 + 0.32 * face_size + 0.22 * brightness + 0.16 * saturation + 0.05 * contrast),
                "agreeableness": _clamp(0.25 + 0.25 * brightness + 0.25 * face_center + 0.15 * color_balance + 0.10 * saturation),
                "neuroticism": _clamp(0.20 + 0.28 * darkness + 0.25 * blur + 0.17 * off_center + 0.10 * contrast),
            }
        )
    return labels


def prepare_subset(
    output_dir: Path,
    sample_count: int = 700,
    seed: int = 42,
    image_size: int = 160,
    val_ratio: float = 0.2,
) -> Path:
    random.seed(seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    image_dir = output_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    samples = build_samples(
        DEFAULT_CONFIG.train_dir,
        DEFAULT_CONFIG.train_annotation,
        limit_ratio=1.0,
        seed=seed,
    )
    random.shuffle(samples)
    selected = samples[: min(sample_count, len(samples))]
    if not selected:
        raise RuntimeError("No labeled First Impressions samples were found.")

    rows = []
    feature_rows = []
    for index, sample in enumerate(selected, start=1):
        image = load_media(sample.path).resize((image_size, image_size))
        image_name = f"{sample.path.stem}_{index:04d}.jpg"
        relative_image_path = Path("images") / image_name
        image.save(output_dir / relative_image_path, format="JPEG", quality=92)

        row = {
            "image": str(relative_image_path).replace("\\", "/"),
            "source_media": sample.path.name,
        }
        rows.append(row)
        feature_rows.append(_raw_visual_features(image))

    for row, labels in zip(rows, _pseudo_labels(feature_rows)):
        row.update(labels)

    split_at = max(1, int(len(rows) * (1.0 - val_ratio)))
    for split, split_rows in (("train", rows[:split_at]), ("val", rows[split_at:])):
        with open(output_dir / f"{split}_labels.csv", "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["image", "source_media", *TRAIT_ORDER])
            writer.writeheader()
            writer.writerows(split_rows)

    with open(output_dir / "labels.json", "w", encoding="utf-8") as handle:
        json.dump(
            {
                "sample_count": len(rows),
                "train_count": split_at,
                "val_count": len(rows) - split_at,
                "seed": seed,
                "image_size": image_size,
                "label_source": "visual_pseudo_labels",
                "label_note": "Original First Impressions annotation pickle in this workspace contains only 0.5 values, so labels are deterministic visual pseudo-labels derived from frame quality and face-framing cues.",
                "trait_order": list(TRAIT_ORDER),
                "rows": rows,
            },
            handle,
            indent=2,
        )

    return output_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a 700-frame CNN subset from First Impressions videos.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_CONFIG.model_dir / "cnn_700")
    parser.add_argument("--sample-count", type=int, default=700)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--image-size", type=int, default=160)
    parser.add_argument("--val-ratio", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = prepare_subset(
        output_dir=args.output_dir,
        sample_count=args.sample_count,
        seed=args.seed,
        image_size=args.image_size,
        val_ratio=args.val_ratio,
    )
    print(f"Prepared CNN subset at {output_dir}")


if __name__ == "__main__":
    main()
