from __future__ import annotations

from torch import nn


class PersonalityMLP(nn.Module):
    def __init__(
        self,
        input_dim: int = 512,
        hidden_dims: tuple[int, int] = (256, 128),
        output_dim: int = 5,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()

        first_hidden, second_hidden = hidden_dims
        self.network = nn.Sequential(
            nn.Linear(input_dim, first_hidden),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(first_hidden, second_hidden),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(second_hidden, output_dim),
            nn.Sigmoid(),
        )

    def forward(self, features):
        return self.network(features)
