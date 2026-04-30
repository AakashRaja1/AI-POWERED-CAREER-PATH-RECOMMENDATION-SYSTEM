#!/usr/bin/env python
"""
GPU-optimized CNN training for personality recognition
Uses CUDA acceleration for fast deep learning training
"""
from pathlib import Path
from train import PersonalityConfig, train

# High-quality training profile optimized for GPU
config = PersonalityConfig(
    train_dir=Path('backend/ml_personality/first-impressions/train'),
    train_annotation=Path('backend/ml_personality/first-impressions/annotations/train-annotation/annotation_training.pkl'),
    subset_ratio=1.0,  # Use all data
    epochs=20,  # Extended training for best quality
    batch_size=48,  # GPU can handle larger batches (9.9 GB available)
    learning_rate=1e-4,  # Fine-tuned learning rate
    patience=8,  # Allow more patience for convergence
    validation_split_ratio=0.15,  # More training data
)

print('='*70)
print('CNN PERSONALITY MODEL - GPU TRAINING')
print('='*70)
print(f'Epochs: {config.epochs}')
print(f'Batch Size: {config.batch_size}')
print(f'Learning Rate: {config.learning_rate}')
print(f'Full Dataset: {config.subset_ratio*100:.0f}%')
print('='*70)

best_model = train(config, model_type='cnn')
print(f'\n✓ Training Complete!')
print(f'✓ Best model saved: {best_model}')
