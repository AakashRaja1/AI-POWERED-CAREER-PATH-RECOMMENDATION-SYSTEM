from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev

TRAITS = (
    "confidence_score",
    "professionalism_score",
    "communication_score",
    "leadership_potential",
)


def _to_float(value: str) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return float(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate multi-rater CSV into JSON labels and quality report.")
    parser.add_argument("--input-csv", type=Path, default=Path("labels_human_template.csv"))
    parser.add_argument("--output-json", type=Path, default=Path("extra_traits_labels_human.json"))
    parser.add_argument("--quality-report", type=Path, default=Path("artifacts/label_quality_report.json"))
    parser.add_argument("--min-raters", type=int, default=2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {args.input_csv}")

    with open(args.input_csv, "r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    aggregated: dict[str, dict[str, float]] = {}
    quality: dict[str, dict[str, float | int]] = {}

    used_rows = 0
    skipped_rows = 0

    for row in rows:
        file_name = (row.get("file_name") or "").strip()
        if not file_name:
            skipped_rows += 1
            continue

        trait_values: dict[str, float] = {}
        row_valid = True

        for trait in TRAITS:
            scores = []
            for key, value in row.items():
                if key.startswith(f"{trait}_r"):
                    parsed = _to_float(value)
                    if parsed is not None:
                        if parsed < 0.0 or parsed > 1.0:
                            raise ValueError(f"{file_name}: {key}={parsed} outside [0,1]")
                        scores.append(parsed)

            if len(scores) < max(1, args.min_raters):
                row_valid = False
                break

            trait_values[trait] = float(mean(scores))
            quality[f"{file_name}:{trait}"] = {
                "num_raters": len(scores),
                "mean": float(mean(scores)),
                "std": float(pstdev(scores)) if len(scores) > 1 else 0.0,
                "min": float(min(scores)),
                "max": float(max(scores)),
            }

        if row_valid:
            aggregated[file_name] = trait_values
            used_rows += 1
        else:
            skipped_rows += 1

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_json, "w", encoding="utf-8") as handle:
        json.dump(aggregated, handle, indent=2)

    report = {
        "summary": {
            "total_rows": len(rows),
            "used_rows": used_rows,
            "skipped_rows": skipped_rows,
            "min_raters_required": max(1, args.min_raters),
            "coverage": float(used_rows / len(rows)) if rows else 0.0,
        },
        "per_item_trait_stats": quality,
    }
    args.quality_report.parent.mkdir(parents=True, exist_ok=True)
    with open(args.quality_report, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    print(f"Saved labels JSON: {args.output_json}")
    print(f"Saved label quality report: {args.quality_report}")
    print(f"Used rows: {used_rows} | Skipped rows: {skipped_rows}")


if __name__ == "__main__":
    main()
