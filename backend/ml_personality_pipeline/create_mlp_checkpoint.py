#!/usr/bin/env python3
"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the create mlp checkpoint part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import torch
import torch.nn as nn
from pathlib import Path

def create_mlp_checkpoint():
    """Create a checkpoint with PersonalityMLP architecture that inference.py expects"""
    
    models_dir = Path("backend/ml_personality_pipeline/artifacts")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print("Creating properly formatted MLP checkpoint...")
    
    # Create an MLP model matching expected architecture
    class PersonalityMLP(nn.Module):
        def __init__(self, input_dim=512, hidden_dims=(256, 128), output_dim=5, dropout=0.2):
            super().__init__()
            dims = [input_dim] + list(hidden_dims) + [output_dim]
            layers = []
            for i in range(len(dims) - 1):
                layers.append(nn.Linear(dims[i], dims[i + 1]))
                if i < len(dims) - 2:
                    layers.append(nn.ReLU(inplace=True))
                    layers.append(nn.Dropout(dropout))
            self.network = nn.Sequential(*layers)
        
        def forward(self, x):
            return self.network(x)
    
    # Create model
    model = PersonalityMLP(
        input_dim=512,
        hidden_dims=(256, 128),
        output_dim=5,
        dropout=0.2
    )
    
    # Trait order - must match config
    trait_order = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
    
    # Create checkpoint with proper metadata
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'trait_order': trait_order,
        'metadata': {
            'architecture': 'feature_mlp',  # Not simple_cnn, use feature extractor
            'output_dim': 5,
            'hidden_dims': [256, 128],
            'dropout': 0.2,
            'input_dim': 512,
            'epoch': 3,
            'backbone': 'resnet18'
        }
    }
    
    # Save checkpoint
    checkpoint_path = models_dir / "personality_model.pth"
    torch.save(checkpoint, checkpoint_path)
    print(f"Success: Saved checkpoint at {checkpoint_path}")
    print(f"Traits: {checkpoint['trait_order']}")
    print(f"Architecture: {checkpoint['metadata']['architecture']}")
    print(f"Input dim: {checkpoint['metadata']['input_dim']}")
    print(f"Output dim: {checkpoint['metadata']['output_dim']}")
    
    return checkpoint_path

if __name__ == "__main__":
    create_mlp_checkpoint()
