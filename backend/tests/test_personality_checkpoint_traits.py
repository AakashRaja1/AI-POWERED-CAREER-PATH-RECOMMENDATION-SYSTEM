import tempfile
from pathlib import Path

import torch

from ml_personality_pipeline.model import PersonalityMLP
from ml_personality_pipeline.utils import build_model_from_checkpoint, save_model


def test_checkpoint_loads_dynamic_output_dim():
    model = PersonalityMLP(input_dim=16, hidden_dims=(8, 4), output_dim=9, dropout=0.0)
    trait_order = [f"trait_{i}" for i in range(9)]

    with tempfile.TemporaryDirectory() as tmp_dir:
        model_path = Path(tmp_dir) / "dynamic_traits.pth"
        save_model(
            model,
            model_path,
            metadata={
                "hidden_dims": (8, 4),
                "dropout": 0.0,
                "output_dim": 9,
                "trait_order": trait_order,
            },
            trait_order=trait_order,
        )

        loaded = build_model_from_checkpoint(model_path, input_dim=16)
        sample = torch.randn(2, 16)
        output = loaded(sample)
        assert output.shape == (2, 9)
