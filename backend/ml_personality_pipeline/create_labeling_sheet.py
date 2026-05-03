"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the create labeling sheet part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from dataset_loader import VIDEO_EXTENSIONS, IMAGE_EXTENSIONS

TRAITS = (
    "confidence_score",
    "professionalism_score",
    "communication_score",
    "leadership_potential",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create CSV sheet for human trait annotation.")
    parser.add_argument("--media-dir", type=Path, default=Path("../ml_personality/first-impressions/train"))
    parser.add_argument("--output", type=Path, default=Path("labels_human_template.csv"))
    parser.add_argument("--num-raters", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    media_dir = args.media_dir
    if not media_dir.exists():
        raise FileNotFoundError(f"Media directory not found: {media_dir}")

    file_names = [
        p.name
        for p in sorted(media_dir.iterdir())
        if p.suffix.lower() in VIDEO_EXTENSIONS | IMAGE_EXTENSIONS
    ]
    if not file_names:
        raise ValueError(f"No media files found in {media_dir}")

    header = ["file_name"]
    for trait in TRAITS:
        for rater_idx in range(1, max(1, args.num_raters) + 1):
            header.append(f"{trait}_r{rater_idx}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for file_name in file_names:
            writer.writerow([file_name])

    print(f"Created labeling sheet with {len(file_names)} rows: {args.output}")


if __name__ == "__main__":
    main()
