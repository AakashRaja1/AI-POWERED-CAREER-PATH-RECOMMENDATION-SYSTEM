"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the generate extra labels part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean


def generate(in_csv: Path, out_json: Path) -> None:
    if not in_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {in_csv}")

    with open(in_csv, newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        items = {}
        for row in reader:
            file_name = row.get('file_name')
            if not file_name:
                continue
            # Collect trait prefixes by inspecting columns that end with _rN
            trait_values = {}
            for key, val in row.items():
                if not key or key == 'file_name':
                    continue
                if '_' not in key:
                    continue
                trait, _ = key.rsplit('_', 1)
                try:
                    v = float(val) if val not in (None, '') else None
                except Exception:
                    v = None
                if v is None:
                    continue
                trait_values.setdefault(trait, []).append(v)

            if not trait_values:
                continue

            averaged = {trait: mean(vals) for trait, vals in trait_values.items()}
            items[file_name] = averaged

    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, 'w', encoding='utf-8') as handle:
        json.dump(items, handle, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(description='Generate averaged extra labels JSON from CSV of human raters')
    parser.add_argument('csv', type=Path, help='Input CSV path (template with rater columns)')
    parser.add_argument('out', type=Path, nargs='?', help='Output JSON path', default=Path(__file__).parent / 'artifacts' / 'extra_labels.json')
    return parser.parse_args()


def main():
    args = parse_args()
    generate(args.csv, args.out)
    print(f"Wrote extra labels to {args.out}")


if __name__ == '__main__':
    main()
