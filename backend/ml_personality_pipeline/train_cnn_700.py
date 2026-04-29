from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path
from typing import Sequence

import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

try:
    from .cnn_model import SimplePersonalityCNN
    from .config import DEFAULT_CONFIG, TRAIT_ORDER
    from .prepare_cnn_subset import prepare_subset
    from .utils import ensure_parent
except ImportError:
    from cnn_model import SimplePersonalityCNN
    from config import DEFAULT_CONFIG, TRAIT_ORDER
    from prepare_cnn_subset import prepare_subset
    from utils import ensure_parent


class CNNFrameDataset(Dataset):
    def __init__(self, labels_csv: Path, root_dir: Path, training: bool, image_size: int) -> None:
        self.root_dir = root_dir
        self.rows = self._read_rows(labels_csv)
        self.transform = transforms.Compose(
            [
                transforms.Resize((image_size, image_size)),
                transforms.RandomHorizontalFlip(p=0.5) if training else transforms.Lambda(lambda image: image),
                transforms.ColorJitter(brightness=0.12, contrast=0.12, saturation=0.08) if training else transforms.Lambda(lambda image: image),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ]
        )

    @staticmethod
    def _read_rows(labels_csv: Path) -> list[dict[str, str]]:
        with open(labels_csv, "r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int):
        row = self.rows[index]
        image = Image.open(self.root_dir / row["image"]).convert("RGB")
        target = torch.tensor([float(row[trait]) for trait in TRAIT_ORDER], dtype=torch.float32)
        return self.transform(image), target


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def run_epoch(model, loader, criterion, optimizer=None, device="cpu") -> dict[str, float]:
    training = optimizer is not None
    model.train(mode=training)
    total_loss = 0.0
    total_abs_error = 0.0
    total_items = 0
    total_traits = 0

    for images, targets in loader:
        images = images.to(device)
        targets = targets.to(device)
        predictions = model(images)
        loss = criterion(predictions, targets)

        if training:
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

        batch_size = images.size(0)
        total_loss += float(loss.item()) * batch_size
        total_abs_error += torch.abs(predictions - targets).sum().item()
        total_items += batch_size
        total_traits += targets.numel()

    mae = total_abs_error / max(1, total_traits)
    return {
        "loss": total_loss / max(1, total_items),
        "mae": mae,
        "accuracy": max(0.0, min(1.0, 1.0 - mae)),
    }


def save_checkpoint(model, output_path: Path, metadata: dict, trait_order: Sequence[str]) -> None:
    ensure_parent(output_path)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "metadata": metadata,
            "trait_order": list(trait_order),
        },
        output_path,
    )


def train_cnn(
    subset_dir: Path,
    output_path: Path,
    epochs: int = 18,
    batch_size: int = 16,
    learning_rate: float = 2e-4,
    weight_decay: float = 1e-4,
    patience: int = 5,
    image_size: int = 160,
    seed: int = 42,
    force_prepare: bool = False,
) -> Path:
    set_seed(seed)
    torch.set_num_threads(2)

    if force_prepare or not (subset_dir / "train_labels.csv").exists() or not (subset_dir / "val_labels.csv").exists():
        prepare_subset(output_dir=subset_dir, sample_count=700, seed=seed, image_size=image_size)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_dataset = CNNFrameDataset(subset_dir / "train_labels.csv", subset_dir, training=True, image_size=image_size)
    val_dataset = CNNFrameDataset(subset_dir / "val_labels.csv", subset_dir, training=False, image_size=image_size)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    model = SimplePersonalityCNN(output_dim=len(TRAIT_ORDER), dropout=0.25).to(device)
    criterion = nn.SmoothL1Loss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)

    best_val_loss = math.inf
    bad_epochs = 0
    history = []

    for epoch in range(1, epochs + 1):
        train_metrics = run_epoch(model, train_loader, criterion, optimizer=optimizer, device=device)
        val_metrics = run_epoch(model, val_loader, criterion, device=device)
        scheduler.step(val_metrics["loss"])

        history.append(
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
            f"Epoch {epoch}/{epochs} | train_loss={train_metrics['loss']:.4f} "
            f"| val_loss={val_metrics['loss']:.4f} | val_acc={val_metrics['accuracy']:.4f}"
        )

        if val_metrics["loss"] < best_val_loss:
            best_val_loss = val_metrics["loss"]
            bad_epochs = 0
            save_checkpoint(
                model,
                output_path,
                metadata={
                    "architecture": "simple_cnn",
                    "dataset": "First Impressions 700-frame subset",
                    "subset_dir": str(subset_dir),
                    "sample_count": len(train_dataset) + len(val_dataset),
                    "train_count": len(train_dataset),
                    "val_count": len(val_dataset),
                    "image_size": image_size,
                    "epochs_requested": epochs,
                    "batch_size": batch_size,
                    "learning_rate": learning_rate,
                    "best_val_loss": best_val_loss,
                    "output_dim": len(TRAIT_ORDER),
                },
                trait_order=TRAIT_ORDER,
            )
        else:
            bad_epochs += 1
            if bad_epochs >= patience:
                print("Early stopping triggered.")
                break

    report_path = output_path.parent / "cnn_training_report.json"
    ensure_parent(report_path)
    with open(report_path, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "summary": {
                    "best_model_path": str(output_path),
                    "best_val_loss": best_val_loss,
                    "epochs_completed": len(history),
                    "device": device,
                },
                "epochs": history,
            },
            handle,
            indent=2,
        )
    print(f"Saved CNN model to {output_path}")
    print(f"Saved training report to {report_path}")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a CNN on 700 First Impressions frames.")
    parser.add_argument("--subset-dir", type=Path, default=DEFAULT_CONFIG.model_dir / "cnn_700")
    parser.add_argument("--output-path", type=Path, default=DEFAULT_CONFIG.model_path)
    parser.add_argument("--epochs", type=int, default=18)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--patience", type=int, default=5)
    parser.add_argument("--image-size", type=int, default=160)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--force-prepare", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train_cnn(
        subset_dir=args.subset_dir,
        output_path=args.output_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        patience=args.patience,
        image_size=args.image_size,
        seed=args.seed,
        force_prepare=args.force_prepare,
    )


if __name__ == "__main__":
    main()
