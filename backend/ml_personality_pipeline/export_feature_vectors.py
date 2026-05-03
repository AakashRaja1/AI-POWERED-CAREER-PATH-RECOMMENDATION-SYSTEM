"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the export feature vectors part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from config import DEFAULT_CONFIG
from dataset_loader import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS, load_media_frames
from feature_extractor import ResNet18FeatureExtractor
from preprocessing import build_transforms


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export media feature vectors (ResNet18 embeddings) for viva/demo.")
    parser.add_argument("--media-dir", type=Path, default=Path("../ml_personality/first-impressions/train"))
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument("--frames-per-video", type=int, default=6)
    parser.add_argument("--output", type=Path, default=Path("artifacts/feature_vectors.pt"))
    parser.add_argument("--meta-output", type=Path, default=Path("artifacts/feature_vectors_meta.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.media_dir.exists():
        raise FileNotFoundError(f"Media dir not found: {args.media_dir}")

    candidates = [
        p for p in sorted(args.media_dir.iterdir()) if p.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
    ]
    if not candidates:
        raise ValueError(f"No media files found in {args.media_dir}")

    selected = candidates[: max(1, args.max_files)]

    transform = build_transforms(training=False)
    feature_extractor = ResNet18FeatureExtractor().to("cpu")
    feature_extractor.eval()

    filenames: list[str] = []
    vectors: list[torch.Tensor] = []

    with torch.no_grad():
        for media_path in selected:
            frames = load_media_frames(media_path, max_frames=max(1, args.frames_per_video))
            frame_tensor = torch.stack([transform(img) for img in frames], dim=0)
            frame_features = feature_extractor(frame_tensor)
            media_feature = frame_features.mean(dim=0).cpu()

            filenames.append(media_path.name)
            vectors.append(media_feature)

    matrix = torch.stack(vectors, dim=0)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "filenames": filenames,
            "vectors": matrix,
            "feature_dim": int(matrix.shape[1]),
            "num_samples": int(matrix.shape[0]),
        },
        args.output,
    )

    args.meta_output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.meta_output, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "media_dir": str(args.media_dir),
                "num_files": len(filenames),
                "feature_dim": int(matrix.shape[1]),
                "frames_per_video": max(1, args.frames_per_video),
                "output_tensor": str(args.output),
            },
            handle,
            indent=2,
        )

    print(f"Exported vectors: {args.output}")
    print(f"Exported vector metadata: {args.meta_output}")
    print(f"Samples={matrix.shape[0]} | FeatureDim={matrix.shape[1]}")


if __name__ == "__main__":
    main()
