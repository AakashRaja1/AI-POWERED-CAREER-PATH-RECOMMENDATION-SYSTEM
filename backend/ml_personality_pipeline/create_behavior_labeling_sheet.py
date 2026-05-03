from __future__ import annotations

import argparse
import csv
from pathlib import Path

from dataset_loader import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS


TRAITS = (
    "face_visibility",
    "smile_positive_expression",
    "face_centering",
    "face_size",
    "head_movement",
    "audio_speaking_rhythm",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create CSV sheet for human behavior-cue annotation.")
    parser.add_argument("--media-dir", type=Path, default=Path("../ml_personality/first-impressions/train"))
    parser.add_argument("--output", type=Path, default=Path("behavior_labels_human_template.csv"))
    parser.add_argument("--num-raters", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    media_dir = args.media_dir
    if not media_dir.exists():
        raise FileNotFoundError(f"Media directory not found: {media_dir}")

    file_names = [
        path.name
        for path in sorted(media_dir.iterdir())
        if path.suffix.lower() in VIDEO_EXTENSIONS | IMAGE_EXTENSIONS
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

    print(f"Created behavior labeling sheet with {len(file_names)} rows: {args.output}")


if __name__ == "__main__":
    main()