from pathlib import Path
from train import PersonalityConfig, train

config = PersonalityConfig(
    train_dir=Path('backend/ml_personality/first-impressions/train'),
    train_annotation=Path('backend/ml_personality/first-impressions/annotations/train-annotation/annotation_training.pkl'),
    subset_ratio=1.0,
    epochs=5,
    batch_size=16,
    validation_split_ratio=0.2,
)

print('Starting training with config:')
print(config)

best = train(config, model_type='cnn')
print('Best model saved to', best)
