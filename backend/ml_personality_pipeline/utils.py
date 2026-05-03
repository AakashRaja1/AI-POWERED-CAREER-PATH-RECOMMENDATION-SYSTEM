"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the utils part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Sequence

import torch

try:
    from .config import DEFAULT_CONFIG, TRAIT_ORDER
    from .model import PersonalityMLP
except ImportError:
    from config import DEFAULT_CONFIG, TRAIT_ORDER
    from model import PersonalityMLP


def ensure_parent(path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)


def save_model(
    model: torch.nn.Module,
    path: Path | str,
    metadata: Dict[str, Any] | None = None,
    trait_order: Sequence[str] | None = None,
) -> Path:
    path = Path(path)
    ensure_parent(path)
    resolved_trait_order = list(trait_order) if trait_order is not None else list(TRAIT_ORDER)
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "metadata": metadata or {},
        "trait_order": resolved_trait_order,
    }
    torch.save(checkpoint, path)
    return path


def load_checkpoint(path: Path | str) -> Dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {path}")
    return torch.load(path, map_location="cpu")


def build_model_from_checkpoint(path: Path | str, input_dim: int = 512) -> PersonalityMLP:
    checkpoint = load_checkpoint(path)
    metadata = checkpoint.get("metadata", {})
    hidden_dims = tuple(metadata.get("hidden_dims", DEFAULT_CONFIG.hidden_dims))
    dropout = float(metadata.get("dropout", DEFAULT_CONFIG.dropout))
    trait_order = tuple(checkpoint.get("trait_order") or metadata.get("trait_order") or TRAIT_ORDER)
    output_dim = int(metadata.get("output_dim", len(trait_order)))
    model = PersonalityMLP(
        input_dim=input_dim,
        hidden_dims=hidden_dims,
        output_dim=output_dim,
        dropout=dropout,
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model


def clamp_traits(values: Iterable[float]) -> list[float]:
    return [max(0.0, min(1.0, float(value))) for value in values]
