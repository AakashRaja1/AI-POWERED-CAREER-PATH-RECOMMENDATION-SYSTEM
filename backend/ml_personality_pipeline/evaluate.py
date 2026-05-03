"""
Evaluation script for trained personality models. It measures prediction quality and writes reports that can be discussed during presentation.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Sequence

import torch
from torch.utils.data import DataLoader

try:
    from .config import DEFAULT_CONFIG, TRAIT_ORDER, PersonalityConfig
    from .dataset_loader import FirstImpressionsDataset, build_samples, load_extra_labels
    from .feature_extractor import ResNet18FeatureExtractor
    from .preprocessing import build_transforms
    from .utils import ensure_parent, load_checkpoint, build_model_from_checkpoint
except ImportError:
    from config import DEFAULT_CONFIG, TRAIT_ORDER, PersonalityConfig
    from dataset_loader import FirstImpressionsDataset, build_samples, load_extra_labels
    from feature_extractor import ResNet18FeatureExtractor
    from preprocessing import build_transforms
    from utils import ensure_parent, load_checkpoint, build_model_from_checkpoint


def _pearson(x: torch.Tensor, y: torch.Tensor) -> float:
    if x.numel() < 2 or y.numel() < 2:
        return 0.0

    x_centered = x - x.mean()
    y_centered = y - y.mean()

    denominator = torch.sqrt((x_centered.pow(2).sum()) * (y_centered.pow(2).sum()))
    if denominator.item() == 0.0:
        return 0.0

    correlation = (x_centered * y_centered).sum() / denominator
    return float(correlation.item())


def _split_paths(config: PersonalityConfig) -> dict[str, tuple[Path, Path]]:
    return {
        "train": (config.train_dir, config.train_annotation),
        "val": (config.val_dir, config.val_annotation),
        "test": (config.test_dir, config.test_annotation),
    }


def evaluate(
    config: PersonalityConfig,
    model_path: Path,
    split: str = "train",
    report_path: Path | None = None,
) -> dict:
    checkpoint = load_checkpoint(model_path)
    metadata = checkpoint.get("metadata", {})
    checkpoint_trait_order = tuple(checkpoint.get("trait_order") or metadata.get("trait_order") or TRAIT_ORDER)

    extra_trait_order = tuple(str(name) for name in config.extra_trait_order)
    target_trait_order = tuple(TRAIT_ORDER) + extra_trait_order

    missing_traits = [trait for trait in target_trait_order if trait not in checkpoint_trait_order]
    if missing_traits:
        raise ValueError(
            "Checkpoint is missing target traits: "
            f"{missing_traits}. Check your --extra-traits or checkpoint model."
        )

    index_map = [checkpoint_trait_order.index(trait) for trait in target_trait_order]

    split_paths = _split_paths(config)
    if split not in split_paths:
        raise ValueError(f"Unknown split '{split}'. Choose from: train, val, test")

    split_dir, annotation_path = split_paths[split]

    extra_labels = None
    if extra_trait_order:
        if config.extra_labels_json is None:
            raise ValueError("extra_labels_json is required when extra_trait_order is provided")
        extra_labels = load_extra_labels(config.extra_labels_json)

    samples = build_samples(
        split_dir=split_dir,
        annotation_path=annotation_path,
        limit_ratio=config.subset_ratio,
        seed=config.seed,
        extra_labels=extra_labels,
        extra_trait_order=extra_trait_order,
    )

    dataset = FirstImpressionsDataset(
        split_dir=split_dir,
        annotation_path=annotation_path,
        transform=build_transforms(training=False),
        samples=samples,
        extra_labels=extra_labels,
        extra_trait_order=extra_trait_order,
    )
    loader = DataLoader(
        dataset,
        batch_size=min(max(1, config.batch_size), 16),
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )

    feature_extractor = ResNet18FeatureExtractor().to("cpu")
    model = build_model_from_checkpoint(model_path, input_dim=feature_extractor.feature_dim).to("cpu")
    feature_extractor.eval()
    model.eval()

    prediction_batches: list[torch.Tensor] = []
    target_batches: list[torch.Tensor] = []

    with torch.no_grad():
        for images, targets, _ in loader:
            features = feature_extractor(images.to("cpu"))
            predictions = model(features)
            selected_predictions = predictions[:, index_map]
            selected_predictions = torch.clamp(selected_predictions, 0.0, 1.0)

            prediction_batches.append(selected_predictions.cpu())
            target_batches.append(targets.to("cpu"))

    if not prediction_batches:
        raise ValueError("No samples found for evaluation. Check split paths and labels.")

    y_pred = torch.cat(prediction_batches, dim=0)
    y_true = torch.cat(target_batches, dim=0)

    error = y_pred - y_true
    abs_error = error.abs()
    sq_error = error.pow(2)

    trait_metrics: dict[str, dict[str, float]] = {}
    for idx, trait_name in enumerate(target_trait_order):
        pred_col = y_pred[:, idx]
        true_col = y_true[:, idx]
        trait_metrics[trait_name] = {
            "mae": float(abs_error[:, idx].mean().item()),
            "rmse": float(torch.sqrt(sq_error[:, idx].mean()).item()),
            "pearson": _pearson(pred_col, true_col),
        }

    report = {
        "summary": {
            "split": split,
            "num_samples": int(y_true.shape[0]),
            "num_traits": int(y_true.shape[1]),
            "overall_mae": float(abs_error.mean().item()),
            "overall_rmse": float(torch.sqrt(sq_error.mean()).item()),
            "model_path": str(model_path),
            "checkpoint_trait_order": list(checkpoint_trait_order),
            "evaluated_trait_order": list(target_trait_order),
        },
        "traits": trait_metrics,
    }

    if report_path is not None:
        ensure_parent(report_path)
        with open(report_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)

    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate personality model per trait.")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_CONFIG.model_path)
    parser.add_argument("--split", type=str, choices=["train", "val", "test"], default="train")
    parser.add_argument("--subset-ratio", type=float, default=1.0)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_CONFIG.batch_size)
    parser.add_argument("--extra-labels-json", type=Path, default=None)
    parser.add_argument(
        "--extra-traits",
        type=str,
        default="",
        help="Comma-separated extra traits used during training/evaluation.",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=None,
        help="Optional output JSON path. Default: artifacts/evaluation_report_<split>.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    extra_trait_order = tuple(t.strip() for t in args.extra_traits.split(",") if t.strip())

    config = PersonalityConfig(
        subset_ratio=args.subset_ratio,
        batch_size=args.batch_size,
        extra_trait_order=extra_trait_order,
        extra_labels_json=args.extra_labels_json,
    )

    report_path = args.report_path
    if report_path is None:
        report_path = DEFAULT_CONFIG.model_dir / f"evaluation_report_{args.split}.json"

    report = evaluate(
        config=config,
        model_path=args.model_path,
        split=args.split,
        report_path=report_path,
    )

    print(
        f"Split={report['summary']['split']} | "
        f"Samples={report['summary']['num_samples']} | "
        f"Overall MAE={report['summary']['overall_mae']:.4f} | "
        f"Overall RMSE={report['summary']['overall_rmse']:.4f}"
    )
    print(f"Saved evaluation report to {report_path}")


if __name__ == "__main__":
    main()
