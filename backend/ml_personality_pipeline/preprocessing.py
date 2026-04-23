from __future__ import annotations

from torchvision import transforms


IMAGE_NET_MEAN = (0.485, 0.456, 0.406)
IMAGE_NET_STD = (0.229, 0.224, 0.225)


def build_transforms(training: bool = False) -> transforms.Compose:
    steps = []
    if training:
        steps.append(transforms.RandomHorizontalFlip(p=0.5))

    steps.extend(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGE_NET_MEAN, std=IMAGE_NET_STD),
        ]
    )
    return transforms.Compose(steps)
