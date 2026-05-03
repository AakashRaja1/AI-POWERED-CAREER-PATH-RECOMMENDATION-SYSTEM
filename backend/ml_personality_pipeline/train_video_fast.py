#!/usr/bin/env python3
"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the train video fast part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml_personality_pipeline.video_training import (
    VideoTrainingConfig,
    build_config,
    train_video_model,
)

def main():
    """Train model with fast CPU-friendly settings."""
    
    # Override config for fast training
    config_dict = {
        "use_subset": True,
        "subset_size": 100,  # Small but meaningful subset
        "random_seed": 42,
        "frames_per_video": 8,  # Fewer frames
        "img_size": 224,
        "train_split": 0.7,
        "val_split": 0.15,
        "test_split": 0.15,
        "backbone": "efficientnet_b0",
        "batch_size": 8,
        "epochs": 3,
        "lr": 5e-5,
        "dropout": 0.3,
    }
    
    config = VideoTrainingConfig(**config_dict)
    print(f"\n{'='*70}")
    print("FAST VIDEO TRAINING - CPU OPTIMIZED")
    print(f"{'='*70}")
    print(f"Backbone: {config.backbone}")
    print(f"Dataset: {config.subset_size} videos (train/val/test: {config.train_split}/{config.val_split}/{config.test_split})")
    print(f"Epochs: {config.epochs}")
    print(f"Batch Size: {config.batch_size}")
    print(f"Frames/Video: {config.frames_per_video}")
    print(f"{'='*70}\n")
    
    # Run training
    train_video_model(config)
    
    print(f"\n{'='*70}")
    print("TRAINING COMPLETE")
    print(f"{'='*70}")
    print(f"✓ Model checkpoint: backend/ml_personality_pipeline/models/model_v2_best.pth")
    print(f"✓ Metrics: backend/ml_personality_pipeline/artifacts/video_v2/metrics.json")
    print(f"✓ Plots: backend/ml_personality_pipeline/artifacts/video_v2/*.png")
    print(f"✓ Predictions: backend/ml_personality_pipeline/artifacts/video_v2/test_predictions.csv")
    print(f"✓ Config: backend/ml_personality_pipeline/artifacts/video_v2/run_config_snapshot.yaml")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
