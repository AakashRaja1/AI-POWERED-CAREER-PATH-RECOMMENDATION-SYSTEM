"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the cnn pipeline part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import csv
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import torch
from PIL import Image, UnidentifiedImageError
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.dataloader import default_collate
from torchvision import transforms
from torchvision.models import ResNet18_Weights, resnet18


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


@dataclass(frozen=True)
class CnnPaths:
    dataset_root: Path
    labels_csv: Path
    outputs_root: Path
    models_dir: Path
    logs_dir: Path
    plots_dir: Path


@dataclass(frozen=True)
class CsvSample:
    image_path: Path
    label_text: str


class CsvImageDataset(Dataset):
    def __init__(self, samples: Sequence[CsvSample], class_to_idx: dict[str, int], transform=None) -> None:
        self.samples = list(samples)
        self.class_to_idx = class_to_idx
        self.transform = transform

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        sample = self.samples[index]
        try:
            image = Image.open(sample.image_path).convert("RGB")
        except (FileNotFoundError, OSError, UnidentifiedImageError):
            return None

        if self.transform is not None:
            image = self.transform(image)

        return image, self.class_to_idx[sample.label_text], str(sample.image_path)


def safe_collate(batch):
    filtered_batch = [item for item in batch if item is not None]
    if not filtered_batch:
        return None
    return default_collate(filtered_batch)


def build_cnn_paths(dataset_root: Path, labels_csv: Path, outputs_root: Path) -> CnnPaths:
    models_dir = outputs_root / "models"
    logs_dir = outputs_root / "logs"
    plots_dir = outputs_root / "plots"

    for directory in (models_dir, logs_dir, plots_dir):
        directory.mkdir(parents=True, exist_ok=True)

    return CnnPaths(
        dataset_root=dataset_root,
        labels_csv=labels_csv,
        outputs_root=outputs_root,
        models_dir=models_dir,
        logs_dir=logs_dir,
        plots_dir=plots_dir,
    )


def _read_csv_rows(labels_csv: Path) -> list[dict[str, str]]:
    if not labels_csv.exists():
        raise FileNotFoundError(f"Labels CSV not found: {labels_csv}")

    with labels_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            normalized = {str(k).strip().lower(): str(v).strip() for k, v in row.items() if k is not None}
            if any(value for value in normalized.values()):
                rows.append(normalized)

    if not rows:
        raise ValueError(f"No rows found in CSV: {labels_csv}")

    return rows


def _pick_column(columns: Iterable[str], candidates: Sequence[str], required_name: str) -> str:
    available = {column.lower().strip() for column in columns}
    for candidate in candidates:
        if candidate in available:
            return candidate
    raise ValueError(f"Missing required column for {required_name}. Available columns: {sorted(available)}")


def _resolve_image_path(dataset_root: Path, file_name_value: str) -> Path:
    candidate = Path(file_name_value)
    if candidate.is_absolute():
        return candidate

    direct = (dataset_root / candidate).resolve()
    if direct.exists():
        return direct

    images_subdir = (dataset_root / "images" / candidate).resolve()
    if images_subdir.exists():
        return images_subdir

    return direct


def load_csv_samples(
    dataset_root: Path,
    labels_csv: Path,
    filename_column: str | None = None,
    label_column: str | None = None,
) -> tuple[list[CsvSample], dict[str, int], dict[str, int], str | None]:
    rows = _read_csv_rows(labels_csv)
    columns = rows[0].keys()

    filename_column = filename_column or _pick_column(
        columns,
        ["filename", "file", "image", "image_path", "path"],
        "filename",
    )
    label_column = label_column or _pick_column(
        columns,
        ["label", "class", "target"],
        "label",
    )

    split_column = None
    for candidate in ("split", "set", "subset"):
        if candidate in columns:
            split_column = candidate
            break

    valid_samples: list[CsvSample] = []
    skipped_missing = 0

    for row in rows:
        file_name = row.get(filename_column, "")
        label_text = row.get(label_column, "")
        if not file_name or not label_text:
            continue

        image_path = _resolve_image_path(dataset_root, file_name)
        if not image_path.exists():
            skipped_missing += 1
            continue

        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        valid_samples.append(CsvSample(image_path=image_path, label_text=label_text))

    if not valid_samples:
        raise ValueError("No valid image samples found after CSV parsing")

    class_names = sorted({sample.label_text for sample in valid_samples})
    class_to_idx = {class_name: idx for idx, class_name in enumerate(class_names)}

    stats = {
        "rows_total": len(rows),
        "rows_valid": len(valid_samples),
        "rows_skipped_missing": skipped_missing,
        "num_classes": len(class_names),
    }

    return valid_samples, class_to_idx, stats, split_column


def build_transforms(training: bool = False) -> transforms.Compose:
    if training:
        return transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomRotation(degrees=15),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ]
        )

    return transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ]
    )


def split_samples(
    samples: Sequence[CsvSample],
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> tuple[list[CsvSample], list[CsvSample], list[CsvSample]]:
    if not 0.0 <= test_ratio < 1.0:
        raise ValueError("test_ratio must be in [0, 1)")
    if not 0.0 <= val_ratio < 1.0:
        raise ValueError("val_ratio must be in [0, 1)")
    if test_ratio + val_ratio >= 1.0:
        raise ValueError("val_ratio + test_ratio must be < 1.0")

    sample_list = list(samples)
    labels = [sample.label_text for sample in sample_list]

    holdout_ratio = val_ratio + test_ratio
    if holdout_ratio == 0:
        return sample_list, [], []

    indices = list(range(len(sample_list)))

    try:
        train_indices, holdout_indices = train_test_split(
            indices,
            test_size=holdout_ratio,
            random_state=seed,
            shuffle=True,
            stratify=labels,
        )
    except ValueError:
        train_indices, holdout_indices = train_test_split(
            indices,
            test_size=holdout_ratio,
            random_state=seed,
            shuffle=True,
            stratify=None,
        )

    if test_ratio == 0 or not holdout_indices:
        val_indices = holdout_indices
        test_indices = []
    else:
        holdout_labels = [labels[i] for i in holdout_indices]
        test_share = test_ratio / holdout_ratio
        try:
            val_indices, test_indices = train_test_split(
                holdout_indices,
                test_size=test_share,
                random_state=seed,
                shuffle=True,
                stratify=holdout_labels,
            )
        except ValueError:
            val_indices, test_indices = train_test_split(
                holdout_indices,
                test_size=test_share,
                random_state=seed,
                shuffle=True,
                stratify=None,
            )

    train_samples = [sample_list[i] for i in train_indices]
    val_samples = [sample_list[i] for i in val_indices]
    test_samples = [sample_list[i] for i in test_indices]

    if not train_samples:
        raise ValueError("Training split is empty. Check dataset size and split ratios.")

    return train_samples, val_samples, test_samples


def create_split_dataloaders(
    samples: Sequence[CsvSample],
    class_to_idx: dict[str, int],
    batch_size: int,
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> tuple[dict[str, DataLoader], dict[str, int]]:
    train_samples, val_samples, test_samples = split_samples(samples, val_ratio=val_ratio, test_ratio=test_ratio, seed=seed)

    split_to_samples = {
        "train": train_samples,
        "val": val_samples,
        "test": test_samples,
    }

    loaders: dict[str, DataLoader] = {}
    split_sizes: dict[str, int] = {}

    for split_name, split_samples_ in split_to_samples.items():
        if not split_samples_:
            continue

        dataset = CsvImageDataset(
            samples=split_samples_,
            class_to_idx=class_to_idx,
            transform=build_transforms(training=(split_name == "train")),
        )

        loaders[split_name] = DataLoader(
            dataset,
            batch_size=min(max(1, int(batch_size)), 8),
            shuffle=(split_name == "train"),
            num_workers=0,
            pin_memory=False,
            collate_fn=safe_collate,
        )
        split_sizes[split_name] = len(split_samples_)

    return loaders, split_sizes


def build_resnet18_classifier(num_classes: int, dropout: float = 0.3, freeze_until: str = "layer2") -> nn.Module:
    try:
        backbone = resnet18(weights=ResNet18_Weights.DEFAULT)
    except Exception:
        backbone = resnet18(weights=None)

    freeze_prefixes = {
        "conv1": ("conv1", "bn1"),
        "layer1": ("conv1", "bn1", "layer1"),
        "layer2": ("conv1", "bn1", "layer1", "layer2"),
        "layer3": ("conv1", "bn1", "layer1", "layer2", "layer3"),
    }
    prefixes = freeze_prefixes.get(freeze_until, freeze_prefixes["layer2"])

    for name, parameter in backbone.named_parameters():
        parameter.requires_grad = not any(name.startswith(prefix) for prefix in prefixes)

    in_features = backbone.fc.in_features
    backbone.fc = nn.Sequential(
        nn.Dropout(p=float(dropout)),
        nn.Linear(in_features, int(num_classes)),
    )
    return backbone


def _run_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer | None,
) -> dict[str, float]:
    is_training = optimizer is not None
    model.train(mode=is_training)

    running_loss = 0.0
    running_correct = 0
    running_total = 0

    for batch in loader:
        if batch is None:
            continue
        images, labels, _ = batch
        images = images.to("cpu")
        labels = labels.to("cpu")

        if is_training:
            optimizer.zero_grad(set_to_none=True)

        logits = model(images)
        loss = criterion(logits, labels)

        if is_training:
            loss.backward()
            optimizer.step()

        predictions = logits.argmax(dim=1)
        running_correct += int((predictions == labels).sum().item())
        running_total += int(labels.size(0))
        running_loss += float(loss.item()) * int(labels.size(0))

    mean_loss = running_loss / max(1, running_total)
    accuracy = running_correct / max(1, running_total)

    return {
        "loss": mean_loss,
        "accuracy": accuracy,
        "samples": running_total,
    }


def _save_training_plot(history: list[dict], output_path: Path) -> None:
    import matplotlib.pyplot as plt

    epochs = [row["epoch"] for row in history]
    train_loss = [row["train_loss"] for row in history]
    val_loss = [row["val_loss"] for row in history]
    train_acc = [row["train_accuracy"] for row in history]
    val_acc = [row["val_accuracy"] for row in history]

    figure, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(epochs, train_loss, label="Train Loss")
    axes[0].plot(epochs, val_loss, label="Val Loss")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("CrossEntropy")
    axes[0].legend()

    axes[1].plot(epochs, train_acc, label="Train Accuracy")
    axes[1].plot(epochs, val_acc, label="Val Accuracy")
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].legend()

    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def _collect_predictions(model: nn.Module, loader: DataLoader) -> tuple[list[int], list[int], list[str]]:
    model.eval()
    true_labels: list[int] = []
    predicted_labels: list[int] = []
    file_paths: list[str] = []

    with torch.no_grad():
        for batch in loader:
            if batch is None:
                continue
            images, labels, paths = batch
            logits = model(images.to("cpu"))
            preds = logits.argmax(dim=1).cpu().tolist()
            true = labels.cpu().tolist()

            true_labels.extend(true)
            predicted_labels.extend(preds)
            file_paths.extend(paths)

    return true_labels, predicted_labels, file_paths


def evaluate_classification(
    model: nn.Module,
    loader: DataLoader,
    class_names: Sequence[str],
) -> dict:
    y_true, y_pred, _ = _collect_predictions(model, loader)
    if not y_true:
        raise ValueError("No valid samples were available for evaluation")

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0,
    )

    labels_range = list(range(len(class_names)))
    cm = confusion_matrix(y_true, y_pred, labels=labels_range)
    class_report = classification_report(y_true, y_pred, target_names=list(class_names), zero_division=0, output_dict=True)

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_weighted": float(precision),
        "recall_weighted": float(recall),
        "f1_weighted": float(f1),
        "confusion_matrix": cm.tolist(),
        "classification_report": class_report,
        "samples": len(y_true),
    }


def save_confusion_matrix_plot(confusion: list[list[int]], class_names: Sequence[str], output_path: Path) -> None:
    import matplotlib.pyplot as plt

    matrix = torch.tensor(confusion).cpu().numpy()

    figure, axis = plt.subplots(figsize=(7, 6))
    image = axis.imshow(matrix, cmap="Blues")
    axis.set_title("Confusion Matrix")
    axis.set_xlabel("Predicted")
    axis.set_ylabel("True")
    axis.set_xticks(range(len(class_names)))
    axis.set_yticks(range(len(class_names)))
    axis.set_xticklabels(class_names, rotation=45, ha="right")
    axis.set_yticklabels(class_names)

    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            value = int(matrix[row, col])
            axis.text(col, row, str(value), ha="center", va="center", color="black", fontsize=8)

    figure.colorbar(image, ax=axis)
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def train_cnn_classifier(
    dataset_root: Path,
    labels_csv: Path,
    outputs_root: Path,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    weight_decay: float,
    dropout: float,
    seed: int,
    val_ratio: float,
    test_ratio: float,
    freeze_until: str = "layer2",
) -> Path:
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.set_num_threads(2)

    paths = build_cnn_paths(dataset_root=dataset_root, labels_csv=labels_csv, outputs_root=outputs_root)
    samples, class_to_idx, csv_stats, _ = load_csv_samples(dataset_root=dataset_root, labels_csv=labels_csv)
    class_names = [name for name, _ in sorted(class_to_idx.items(), key=lambda item: item[1])]

    loaders, split_sizes = create_split_dataloaders(
        samples=samples,
        class_to_idx=class_to_idx,
        batch_size=batch_size,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        seed=seed,
    )

    if "train" not in loaders:
        raise ValueError("Train DataLoader was not created")

    model = build_resnet18_classifier(num_classes=len(class_names), dropout=dropout, freeze_until=freeze_until).to("cpu")
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        [parameter for parameter in model.parameters() if parameter.requires_grad],
        lr=learning_rate,
        weight_decay=weight_decay,
    )

    history: list[dict] = []
    best_val_accuracy = -1.0
    model_path = paths.models_dir / "model.pth"

    for epoch in range(1, int(epochs) + 1):
        train_metrics = _run_epoch(model=model, loader=loaders["train"], criterion=criterion, optimizer=optimizer)
        val_metrics = _run_epoch(model=model, loader=loaders.get("val", loaders["train"]), criterion=criterion, optimizer=None)

        row = {
            "epoch": epoch,
            "train_loss": train_metrics["loss"],
            "train_accuracy": train_metrics["accuracy"],
            "val_loss": val_metrics["loss"],
            "val_accuracy": val_metrics["accuracy"],
        }
        history.append(row)

        print(
            f"Epoch {epoch}/{epochs} | "
            f"train_loss={row['train_loss']:.4f} train_acc={row['train_accuracy']:.4f} | "
            f"val_loss={row['val_loss']:.4f} val_acc={row['val_accuracy']:.4f}"
        )

        if row["val_accuracy"] >= best_val_accuracy:
            best_val_accuracy = row["val_accuracy"]
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "class_to_idx": class_to_idx,
                    "metadata": {
                        "task": "cnn_classification",
                        "architecture": "resnet18",
                        "dropout": float(dropout),
                        "freeze_until": freeze_until,
                        "num_classes": len(class_names),
                        "class_names": class_names,
                        "dataset_root": str(dataset_root),
                        "labels_csv": str(labels_csv),
                        "split_sizes": split_sizes,
                    },
                },
                model_path,
            )

    labels_path = paths.models_dir / "labels.txt"
    with labels_path.open("w", encoding="utf-8") as handle:
        for class_name in class_names:
            handle.write(f"{class_to_idx[class_name]}\t{class_name}\n")

    training_log_path = paths.logs_dir / "training_log.json"
    with training_log_path.open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "csv_stats": csv_stats,
                "split_sizes": split_sizes,
                "best_val_accuracy": best_val_accuracy,
                "epochs": history,
            },
            handle,
            indent=2,
        )

    plot_path = paths.plots_dir / "training_curves.png"
    _save_training_plot(history=history, output_path=plot_path)

    if "val" in loaders:
        eval_report = evaluate_classification(model=model, loader=loaders["val"], class_names=class_names)
        evaluation_report_path = paths.logs_dir / "evaluation_val.json"
        with evaluation_report_path.open("w", encoding="utf-8") as handle:
            json.dump(eval_report, handle, indent=2)

        confusion_plot_path = paths.plots_dir / "confusion_matrix_val.png"
        save_confusion_matrix_plot(
            confusion=eval_report["confusion_matrix"],
            class_names=class_names,
            output_path=confusion_plot_path,
        )

    print(f"Saved CNN model to {model_path}")
    print(f"Saved labels mapping to {labels_path}")
    print(f"Saved training log to {training_log_path}")
    print(f"Saved plots to {plot_path.parent}")

    return model_path


def evaluate_cnn_checkpoint(
    model_path: Path,
    dataset_root: Path,
    labels_csv: Path,
    split: str,
    batch_size: int,
    val_ratio: float,
    test_ratio: float,
    seed: int,
    outputs_root: Path,
) -> dict:
    checkpoint = torch.load(model_path, map_location="cpu")
    class_to_idx = checkpoint.get("class_to_idx")
    if not class_to_idx:
        raise ValueError("Checkpoint missing class_to_idx mapping")

    class_names = [name for name, _ in sorted(class_to_idx.items(), key=lambda item: item[1])]

    samples, _, csv_stats, _ = load_csv_samples(dataset_root=dataset_root, labels_csv=labels_csv)
    loaders, split_sizes = create_split_dataloaders(
        samples=samples,
        class_to_idx=class_to_idx,
        batch_size=batch_size,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        seed=seed,
    )

    if split not in loaders:
        raise ValueError(f"Requested split '{split}' is unavailable. Available: {sorted(loaders.keys())}")

    model = build_resnet18_classifier(num_classes=len(class_names), dropout=0.0)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to("cpu")
    model.eval()

    report = evaluate_classification(model=model, loader=loaders[split], class_names=class_names)
    report["split"] = split
    report["split_sizes"] = split_sizes
    report["csv_stats"] = csv_stats
    report["model_path"] = str(model_path)

    paths = build_cnn_paths(dataset_root=dataset_root, labels_csv=labels_csv, outputs_root=outputs_root)
    report_path = paths.logs_dir / f"evaluation_{split}.json"
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    confusion_plot_path = paths.plots_dir / f"confusion_matrix_{split}.png"
    save_confusion_matrix_plot(
        confusion=report["confusion_matrix"],
        class_names=class_names,
        output_path=confusion_plot_path,
    )

    report["report_path"] = str(report_path)
    report["confusion_plot_path"] = str(confusion_plot_path)
    return report


class CNNPersonalityPredictor:
    def __init__(self, model_path: Path) -> None:
        self.model_path = model_path
        checkpoint = torch.load(model_path, map_location="cpu")

        class_to_idx = checkpoint.get("class_to_idx")
        if not class_to_idx:
            raise ValueError(f"Checkpoint does not contain class_to_idx: {model_path}")

        self.idx_to_class = {idx: label for label, idx in class_to_idx.items()}
        self.model = build_resnet18_classifier(num_classes=len(self.idx_to_class), dropout=0.0)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.to("cpu")
        self.model.eval()
        self.transform = build_transforms(training=False)

    def predict(self, image_path: Path) -> dict[str, float | str]:
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = Image.open(image_path).convert("RGB")
        tensor = self.transform(image).unsqueeze(0).to("cpu")

        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1).squeeze(0)
            predicted_idx = int(torch.argmax(probabilities).item())

        return {
            "predicted_label": self.idx_to_class[predicted_idx],
            "confidence": float(probabilities[predicted_idx].item()),
        }
