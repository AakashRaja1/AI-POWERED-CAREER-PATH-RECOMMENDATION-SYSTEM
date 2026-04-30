from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List

try:
    from .config import DEFAULT_CONFIG, TRAIT_ORDER
    from .dataset_loader import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS, load_annotation_mapping
except ImportError:
    from config import DEFAULT_CONFIG, TRAIT_ORDER
    from dataset_loader import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS, load_annotation_mapping


def iter_media_files(split_dir: Path) -> Iterable[Path]:
    for file_path in sorted(split_dir.iterdir()):
        if file_path.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
            yield file_path


def build_split_labels(
    split_dir: Path,
    annotation_path: Path,
    extra_traits: List[str],
    default_extra_value: float,
) -> Dict[str, Dict[str, float]]:
    annotations = load_annotation_mapping(annotation_path)
    trait_maps = {trait: annotations[trait] for trait in TRAIT_ORDER if trait in annotations}

    result: Dict[str, Dict[str, float]] = {}
    for media in iter_media_files(split_dir):
        key = media.name
        if any(key not in trait_map for trait_map in trait_maps.values()):
            continue

        trait_values = {trait: float(trait_maps[trait][key]) for trait in TRAIT_ORDER}
        for extra_trait in extra_traits:
            trait_values[extra_trait] = float(default_extra_value)

        result[key] = trait_values

    return result


def write_json(path: Path, payload: Dict[str, Dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def write_csv(path: Path, payload: Dict[str, Dict[str, float]], trait_order: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file_name", *trait_order])
        writer.writeheader()

        for file_name, traits in payload.items():
            row = {"file_name": file_name}
            row.update({trait: traits[trait] for trait in trait_order})
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate complete label files for train/val/test media from annotation archives."
    )
    parser.add_argument("--output-dir", type=Path, default=Path("labels_generated"))
    parser.add_argument(
        "--extra-traits",
        type=str,
        default="",
        help="Comma-separated extra trait names to include in output with a default value.",
    )
    parser.add_argument(
        "--default-extra-value",
        type=float,
        default=0.5,
        help="Default value to assign for extra traits when generating label templates.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    extra_traits = [item.strip() for item in args.extra_traits.split(",") if item.strip()]

    split_specs = {
        "train": (DEFAULT_CONFIG.train_dir, DEFAULT_CONFIG.train_annotation),
        "val": (DEFAULT_CONFIG.val_dir, DEFAULT_CONFIG.val_annotation),
        "test": (DEFAULT_CONFIG.test_dir, DEFAULT_CONFIG.test_annotation),
    }

    all_labels: Dict[str, Dict[str, float]] = {}
    all_traits_order = list(TRAIT_ORDER) + extra_traits
    split_summary: Dict[str, Dict[str, str | int]] = {}

    for split_name, (split_dir, annotation_path) in split_specs.items():
        try:
            split_labels = build_split_labels(
                split_dir=split_dir,
                annotation_path=annotation_path,
                extra_traits=extra_traits,
                default_extra_value=args.default_extra_value,
            )
        except Exception as error:
            split_summary[split_name] = {
                "status": "skipped",
                "count": 0,
                "reason": str(error),
            }
            print(f"Skipped {split_name} split: {error}")
            continue

        write_json(args.output_dir / f"{split_name}_labels.json", split_labels)
        write_csv(args.output_dir / f"{split_name}_labels.csv", split_labels, all_traits_order)

        for file_name, traits in split_labels.items():
            all_labels[f"{split_name}/{file_name}"] = traits

        split_summary[split_name] = {
            "status": "ok",
            "count": len(split_labels),
            "reason": "",
        }
        print(f"Generated {split_name} labels: {len(split_labels)} items")

    write_json(args.output_dir / "all_labels.json", all_labels)
    write_csv(args.output_dir / "all_labels.csv", all_labels, all_traits_order)
    write_json(args.output_dir / "generation_summary.json", split_summary)
    print(f"Generated combined labels: {len(all_labels)} items")
    print(f"Output directory: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
