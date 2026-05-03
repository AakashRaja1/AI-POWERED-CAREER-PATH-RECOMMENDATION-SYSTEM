"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the cpu train optimal part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import torch
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import PersonalityConfig
from train import train


def main():
    print("="*70)
    print("CPU-OPTIMIZED PERSONALITY CNN TRAINING")
    print("="*70)
    print()
    
    # Check device
    device = torch.device('cpu')
    print(f"Device: {device}")
    print(f"CPU Count: {torch.get_num_threads()} threads")
    print()
    
    # CPU-optimized training profile
    config = PersonalityConfig(
        train_dir=Path('backend/ml_personality/first-impressions/train'),
        train_annotation=Path('backend/ml_personality/first-impressions/annotations/train-annotation/annotation_training.pkl'),
        subset_ratio=1.0,  # Use all data
        epochs=20,  # Standard training
        batch_size=8,  # Smaller batch for CPU memory efficiency
        learning_rate=1e-4,  # Fine-tuned learning rate
        patience=8,  # Early stopping patience
        validation_split_ratio=0.15,  # 15% validation data
    )
    
    print("📋 Training Configuration:")
    print(f"  Model: CNN (ResNet18)")
    print(f"  Device: CPU")
    print(f"  Epochs: {config.epochs}")
    print(f"  Batch Size: {config.batch_size} (CPU-optimized)")
    print(f"  Learning Rate: {config.learning_rate}")
    print(f"  Dataset: 100% ({config.subset_ratio*100:.0f}%)")
    print()
    print("⚠️  Note: CPU training is slower (~50-100 minutes for 20 epochs)")
    print("    Consider using GPU for faster results (gpu_train_optimal.py)")
    print()
    print("-"*70)
    print()
    
    # Train the model
    train(config, model_type='cnn')
    
    print()
    print("="*70)
    print("✅ CPU Training Complete!")
    print("="*70)


if __name__ == "__main__":
    main()
