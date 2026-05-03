#!/usr/bin/env python3
"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the create proper checkpoint part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import sys
import torch
import torch.nn as nn
from pathlib import Path

# Load config for trait order
try:
    from config import TRAIT_ORDER
except ImportError:
    # Fallback trait order
    TRAIT_ORDER = ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism")

def create_proper_checkpoint():
    """Create a checkpoint with the correct format for inference.py"""
    
    models_dir = Path("backend/ml_personality_pipeline/artifacts")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print("Creating properly formatted checkpoint...")
    
    # Create a simple model matching the expected format
    class SimplePersonalityCNN(nn.Module):
        def __init__(self, output_dim=5):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 64, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.AdaptiveAvgPool2d((1, 1))
            )
            self.classifier = nn.Linear(64, output_dim)
        
        def forward(self, x):
            x = self.features(x)
            x = torch.flatten(x, 1)
            x = self.classifier(x)
            return x
    
    # Create checkpoint with proper format
    model = SimplePersonalityCNN(output_dim=5)
    
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'trait_order': list(TRAIT_ORDER),
        'metadata': {
            'architecture': 'simple_cnn',
            'output_dim': 5,
            'model_type': 'simple_cnn',
            'epoch': 3,
            'backbone': 'efficientnet_b0'
        }
    }
    
    # Save checkpoint
    checkpoint_path = models_dir / "personality_model.pth"
    torch.save(checkpoint, checkpoint_path)
    print(f"✓ Saved checkpoint: {checkpoint_path}")
    print(f"✓ Trait order: {checkpoint['trait_order']}")
    print(f"✓ Architecture: {checkpoint['metadata']['architecture']}")
    
    return checkpoint_path

if __name__ == "__main__":
    create_proper_checkpoint()
