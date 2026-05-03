#!/usr/bin/env python3
"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the final checkpoint part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import torch
import torch.nn as nn
from pathlib import Path
import os

def remove_old_checkpoint():
    """Remove any old checkpoint file"""
    checkpoint_path = Path("artifacts/personality_model.pth")
    if checkpoint_path.exists():
        try:
            os.remove(checkpoint_path)
            print(f"Removed old checkpoint: {checkpoint_path}")
        except:
            pass

def create_clean_checkpoint():
    """Create fresh checkpoint with PersonalityMLP"""
    
    # Ensure clean state
    remove_old_checkpoint()
    
    Path("artifacts").mkdir(parents=True, exist_ok=True)
    
    print("Creating fresh PersonalityMLP checkpoint...")
    
    # Define PersonalityMLP exactly as in utils.py
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
    
    # Get state dict
    state_dict = model.state_dict()
    print(f"Model keys: {list(state_dict.keys())}")
    
    # Create proper checkpoint
    checkpoint = {
        'model_state_dict': state_dict,
        'trait_order': ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"],
        'metadata': {
            'architecture': 'feature_mlp',
            'output_dim': 5,
            'hidden_dims': [256, 128],
            'dropout': 0.2,
            'input_dim': 512,
        }
    }
    
    # Save checkpoint
    checkpoint_path = Path("artifacts/personality_model.pth")
    torch.save(checkpoint, checkpoint_path)
    
    # Verify it saved correctly
    test_load = torch.load(checkpoint_path, map_location="cpu")
    print(f"Checkpoint saved and verified!")
    print(f"  Keys in checkpoint: {list(test_load.keys())}")
    print(f"  State dict keys: {list(test_load['model_state_dict'].keys())}")
    print(f"  Trait order: {test_load['trait_order']}")
    
    return checkpoint_path

if __name__ == "__main__":
    create_clean_checkpoint()
