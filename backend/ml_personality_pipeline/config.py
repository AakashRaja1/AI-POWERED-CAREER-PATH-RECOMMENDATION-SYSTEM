from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


PIPELINE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = PIPELINE_DIR.parent
DATASET_ROOT = BACKEND_DIR / "ml_personality" / "first-impressions"
ANNOTATIONS_DIR = DATASET_ROOT / "annotations"
DEFAULT_ARTIFACT_DIR = PIPELINE_DIR / "artifacts"

TRAIT_ORDER: Tuple[str, ...] = (
    "openness",
    "conscientiousness",
    "extraversion",
    "agreeableness",
    "neuroticism",
)


@dataclass(frozen=True)
class PersonalityConfig:
    dataset_root: Path = DATASET_ROOT
    annotations_dir: Path = ANNOTATIONS_DIR
    train_dir: Path = DATASET_ROOT / "train"
    val_dir: Path = DATASET_ROOT / "val"
    test_dir: Path = DATASET_ROOT / "test"
    train_annotation: Path = ANNOTATIONS_DIR / "train-annotation" / "annotation_training.pkl"
    val_annotation: Path = ANNOTATIONS_DIR / "val-annotation-e.zip"
    test_annotation: Path = ANNOTATIONS_DIR / "test-annotation-e.zip"
    model_dir: Path = DEFAULT_ARTIFACT_DIR
    model_path: Path = DEFAULT_ARTIFACT_DIR / "personality_model.pth"
    # High-running default profile for stronger training quality.
    batch_size: int = 8
    epochs: int = 15
    subset_ratio: float = 1.0
    validation_split_ratio: float = 0.2
    learning_rate: float = 5e-4
    weight_decay: float = 1e-4
    patience: int = 5
    num_workers: int = 0
    seed: int = 42
    torch_threads: int = 2
    hidden_dims: Tuple[int, int] = (256, 128)
    dropout: float = 0.2
    # Heavier inference profile: sample more frames per video for stable estimates.
    inference_video_frames: int = 12
    extra_trait_order: Tuple[str, ...] = ()
    extra_labels_json: Optional[Path] = None


DEFAULT_CONFIG = PersonalityConfig()
