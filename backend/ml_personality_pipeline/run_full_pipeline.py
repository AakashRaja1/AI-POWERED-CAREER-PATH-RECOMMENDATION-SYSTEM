"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the run full pipeline part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .process_videos import process_dataset
    from .cnn_pipeline import train_cnn_classifier
    from .config import DEFAULT_CONFIG
except Exception:
    from process_videos import process_dataset
    from cnn_pipeline import train_cnn_classifier
    from config import DEFAULT_CONFIG


def parse_args():
    parser = argparse.ArgumentParser(description="Run extract-frames -> train end-to-end pipeline")
    parser.add_argument("--input-dir", type=Path, default=None, help="Videos root (default: config.dataset_root)")
    parser.add_argument("--annotations", type=Path, required=True, help="Annotation CSV/JSON mapping video->label")
    parser.add_argument("--out-root", type=Path, default=None, help="Output root for processed dataset")
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument("--max-frames-per-video", type=int, default=None)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    return parser.parse_args()


def main():
    args = parse_args()
    config = DEFAULT_CONFIG
    input_dir = Path(args.input_dir) if args.input_dir is not None else config.dataset_root
    out_root = Path(args.out_root) if args.out_root is not None else Path(__file__).resolve().parent / "processed_dataset"

    print("Starting frame extraction...")
    process_dataset(
        input_dir=input_dir,
        annotations_path=args.annotations,
        out_root=out_root,
        fps=args.fps,
        max_frames_per_video=args.max_frames_per_video,
    )

    print("Starting CNN training...")
    model_path = train_cnn_classifier(
        dataset_root=out_root,
        labels_csv=out_root / "labels.csv",
        outputs_root=out_root / "outputs",
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        weight_decay=config.weight_decay,
        dropout=config.dropout,
        seed=config.seed,
        val_ratio=config.cnn_val_ratio,
        test_ratio=config.cnn_test_ratio,
        freeze_until=config.cnn_freeze_until,
    )

    print(f"Pipeline complete. Model saved to: {model_path}")


if __name__ == "__main__":
    main()
