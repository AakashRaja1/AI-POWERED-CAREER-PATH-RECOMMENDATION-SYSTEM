from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Mapping, Sequence

import torch
from torch import nn
from torch.utils.data import DataLoader

from config import DEFAULT_CONFIG, PersonalityConfig, TRAIT_ORDER
from dataset_loader import FirstImpressionsDataset, PersonalitySample, build_samples, load_extra_labels
from feature_extractor import ResNet18FeatureExtractor
from model import PersonalityMLP
from preprocessing import build_transforms
from utils import ensure_parent, save_model


RUN_PROFILES = {
    "light": {
        "subset_ratio": 0.1,
        "epochs": 3,
        "batch_size": 4,
        "learning_rate": 1e-3,
        "patience": 2,
        "validation_split_ratio": 0.2,
    },
    "moderate": {
        "subset_ratio": 0.6,
        "epochs": 8,
        "batch_size": 8,
        "learning_rate": 1e-3,
        "patience": 3,
        "validation_split_ratio": 0.2,
    },
    "high": {
        "subset_ratio": 1.0,
        "epochs": 15,
        "batch_size": 8,
        "learning_rate": 5e-4,
        "patience": 5,
        "validation_split_ratio": 0.2,
    },
}


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def build_dataloader(
    split_dir: Path,
    annotation_path: Path,
    config: PersonalityConfig,
    training: bool,
    samples: Sequence[PersonalitySample] | None = None,
    extra_labels: Mapping[str, Mapping[str, float]] | None = None,
    extra_trait_order: Sequence[str] = (),
) -> DataLoader:
    dataset = FirstImpressionsDataset(
        split_dir=split_dir,
        annotation_path=annotation_path,
        transform=build_transforms(training=training),
        limit_ratio=config.subset_ratio,
        seed=config.seed,
        samples=list(samples) if samples is not None else None,
        extra_labels=extra_labels,
        extra_trait_order=extra_trait_order,
    )
    return DataLoader(
        dataset,
        batch_size=min(config.batch_size, 8),
        shuffle=training,
        num_workers=0,
        pin_memory=False,
    )


def run_epoch(feature_extractor, model, loader, criterion, optimizer=None):
    training = optimizer is not None
    model.train(mode=training)
    feature_extractor.eval()

    total_loss = 0.0
    total_abs_error = 0.0
    total_traits = 0
    total_items = 0

    for images, targets, _ in loader:
        images = images.to("cpu")
        targets = targets.to("cpu")

        with torch.no_grad():
            features = feature_extractor(images)

        predictions = model(features)
        loss = criterion(predictions, targets)
        abs_error = torch.abs(predictions - targets).sum().item()

        if training:
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

        batch_size = images.size(0)
        total_loss += loss.item() * batch_size
        total_abs_error += abs_error
        total_traits += targets.numel()
        total_items += batch_size

    mean_loss = total_loss / max(1, total_items)
    mae = total_abs_error / max(1, total_traits)
    # Accuracy-like score for normalized [0, 1] trait regression.
    accuracy = max(0.0, min(1.0, 1.0 - mae))
    return {
        "loss": mean_loss,
        "mae": mae,
        "accuracy": accuracy,
    }


def train(config: PersonalityConfig = DEFAULT_CONFIG) -> Path:
    set_seed(config.seed)
    torch.set_num_threads(max(1, config.torch_threads))

    full_trait_order = tuple(TRAIT_ORDER) + tuple(config.extra_trait_order)

    extra_labels = None
    if config.extra_trait_order:
        if config.extra_labels_json is None:
            raise ValueError("extra_labels_json is required when extra_trait_order is provided")
        extra_labels = load_extra_labels(config.extra_labels_json)

    feature_extractor = ResNet18FeatureExtractor().to("cpu")
    model = PersonalityMLP(
        input_dim=feature_extractor.feature_dim,
        hidden_dims=config.hidden_dims,
        output_dim=len(full_trait_order),
        dropout=config.dropout,
    ).to("cpu")

    full_samples = build_samples(
        config.train_dir,
        config.train_annotation,
        limit_ratio=config.subset_ratio,
        seed=config.seed,
        extra_labels=extra_labels,
        extra_trait_order=config.extra_trait_order,
    )
    validation_split_ratio = max(0.0, min(0.9, config.validation_split_ratio))
    split_index = max(1, int(len(full_samples) * (1.0 - validation_split_ratio)))
    train_samples = full_samples[:split_index]
    val_samples = full_samples[split_index:]
    if not val_samples:
        val_samples = train_samples[-max(1, len(train_samples) // 5):]

    train_loader = build_dataloader(
        config.train_dir,
        config.train_annotation,
        config,
        training=True,
        samples=train_samples,
        extra_labels=extra_labels,
        extra_trait_order=config.extra_trait_order,
    )
    val_loader = build_dataloader(
        config.train_dir,
        config.train_annotation,
        config,
        training=False,
        samples=val_samples,
        extra_labels=extra_labels,
        extra_trait_order=config.extra_trait_order,
    )

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)

    best_val_loss = math.inf
    epochs_without_improvement = 0
    best_path = config.model_path
    report_rows = []

    for epoch in range(1, config.epochs + 1):
        train_metrics = run_epoch(feature_extractor, model, train_loader, criterion, optimizer=optimizer)
        val_metrics = run_epoch(feature_extractor, model, val_loader, criterion) if val_loader is not None else train_metrics
        train_loss = train_metrics["loss"]
        val_loss = val_metrics["loss"]

        report_rows.append(
            {
                "epoch": epoch,
                "train_loss": train_metrics["loss"],
                "val_loss": val_metrics["loss"],
                "train_mae": train_metrics["mae"],
                "val_mae": val_metrics["mae"],
                "train_accuracy": train_metrics["accuracy"],
                "val_accuracy": val_metrics["accuracy"],
            }
        )

        print(
            f"Epoch {epoch}/{config.epochs} | "
            f"train_loss={train_metrics['loss']:.4f} | val_loss={val_metrics['loss']:.4f} | "
            f"train_acc={train_metrics['accuracy']:.4f} | val_acc={val_metrics['accuracy']:.4f}"
        )

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_without_improvement = 0
            save_model(
                model,
                best_path,
                metadata={
                    "input_dim": feature_extractor.feature_dim,
                    "hidden_dims": config.hidden_dims,
                    "output_dim": len(full_trait_order),
                    "dropout": config.dropout,
                    "batch_size": config.batch_size,
                    "epochs": config.epochs,
                    "subset_ratio": config.subset_ratio,
                    "validation_split_ratio": validation_split_ratio,
                    "trait_order": list(full_trait_order),
                },
                trait_order=full_trait_order,
            )
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= config.patience:
                print("Early stopping triggered.")
                break

    report_path = config.model_dir / "training_report.json"
    ensure_parent(report_path)
    with open(report_path, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "summary": {
                    "epochs_requested": config.epochs,
                    "epochs_completed": len(report_rows),
                    "best_val_loss": best_val_loss,
                    "best_model_path": str(best_path),
                    "used_validation": True,
                    "validation_split_ratio": validation_split_ratio,
                },
                "epochs": report_rows,
            },
            handle,
            indent=2,
        )
    print(f"Saved training report to {report_path}")

    return best_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the First Impressions personality model (high default profile).")
    parser.add_argument(
        "--run-profile",
        type=str,
        choices=["light", "moderate", "high"],
        default="high",
        help="Preset training profile. Individual flags override preset values.",
    )
    parser.add_argument("--subset-ratio", type=float, default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--learning-rate", type=float, default=None)
    parser.add_argument("--patience", type=int, default=None)
    parser.add_argument("--validation-split-ratio", type=float, default=None)
    parser.add_argument("--extra-labels-json", type=Path, default=None)
    parser.add_argument(
        "--extra-traits",
        type=str,
        default="",
        help="Comma-separated extra traits with labels provided in --extra-labels-json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    preset = RUN_PROFILES[args.run_profile]

    subset_ratio = args.subset_ratio if args.subset_ratio is not None else preset["subset_ratio"]
    epochs = args.epochs if args.epochs is not None else preset["epochs"]
    batch_size = args.batch_size if args.batch_size is not None else preset["batch_size"]
    learning_rate = args.learning_rate if args.learning_rate is not None else preset["learning_rate"]
    patience = args.patience if args.patience is not None else preset["patience"]
    validation_split_ratio = (
        args.validation_split_ratio
        if args.validation_split_ratio is not None
        else preset["validation_split_ratio"]
    )

    extra_trait_order = tuple(t.strip() for t in args.extra_traits.split(",") if t.strip())
    config = PersonalityConfig(
        subset_ratio=subset_ratio,
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        patience=patience,
        validation_split_ratio=validation_split_ratio,
        extra_trait_order=extra_trait_order,
        extra_labels_json=args.extra_labels_json,
    )
    model_path = train(config)
    print(f"Saved model to {model_path}")


if __name__ == "__main__":
    main()
