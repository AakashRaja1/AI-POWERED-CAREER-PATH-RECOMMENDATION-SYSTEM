"""
Feature extraction utilities. They convert visual inputs into tensors/features that can be used by training, evaluation, or inference code.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import torch
from torch import nn
from torchvision import models


class ResNet18FeatureExtractor(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        weights = models.ResNet18_Weights.DEFAULT
        backbone = models.resnet18(weights=weights)
        self.feature_dim = backbone.fc.in_features
        backbone.fc = nn.Identity()
        self.backbone = backbone

        for parameter in self.backbone.parameters():
            parameter.requires_grad = False

        self.backbone.eval()

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        features = self.backbone(images)
        if features.ndim > 2:
            features = torch.flatten(features, start_dim=1)
        return features
