from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from typing import Dict, Optional

try:
    # prefer legacy imageio which provides get_reader; fall back to imageio.v3
    import imageio as iio
except Exception:  # pragma: no cover - optional dependency
    try:
        import imageio.v3 as iio
    except Exception:
        iio = None

try:
    from .config import DEFAULT_CONFIG
    from .dataset_loader import load_annotation_mapping
except Exception:
    from config import DEFAULT_CONFIG
    from dataset_loader import load_annotation_mapping


def load_labels_from_csv_or_json(path: Path) -> Dict[str, str]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Annotation file not found: {path}")

    suffix = path.suffix.lower()
    if suffix in (".csv", ".tsv"):
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        mapping = {}
        # attempt to guess columns
        cols = [c.lower().strip() for c in (rows[0].keys() if rows else [])]
        filename_col = None
        label_col = None
        for candidate in ("filename", "file", "video", "video_id", "image"):
            if candidate in cols:
                filename_col = candidate
                break
        for candidate in ("label", "class", "target"):
            if candidate in cols:
                label_col = candidate
                break
        if filename_col is None or label_col is None:
            # fallback: assume first two columns
            if rows and len(rows[0].keys()) >= 2:
                col_list = list(rows[0].keys())
                filename_col = col_list[0]
                label_col = col_list[1]
            else:
                raise ValueError("Could not detect filename/label columns in CSV annotation")

        for row in rows:
            key = str(row[filename_col]).strip()
            val = str(row[label_col]).strip()
            if key:
                mapping[key] = val
        return mapping

    if suffix in (".json",):
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict):
            # assume mapping file_name->label
            return {str(k): str(v) for k, v in payload.items()}
        if isinstance(payload, list):
            mapping = {}
            # assume list of records
            for rec in payload:
                if not isinstance(rec, dict):
                    continue
                keys = list(rec.keys())
                if "filename" in rec and "label" in rec:
                    mapping[str(rec["filename"])]=str(rec["label"]) 
                    continue
                # else if has at least two items
                if len(keys) >= 2:
                    mapping[str(rec[keys[0]])] = str(rec[keys[1]])
            return mapping

    # fallback to pickle/zip like original pipeline
    try:
        annotations = load_annotation_mapping(path)
    except Exception as exc:
        raise RuntimeError(f"Unsupported annotation format: {path} ({exc})") from exc

    # annotations may be nested trait dicts; map to a single label if possible
    mapping = {}
    # if annotations is mapping of trait->mapping(video->float)
    if annotations and isinstance(list(annotations.values())[0], dict):
        # try to collapse into single label by selecting a trait or averaging --- default: pick first trait
        trait = next(iter(annotations.keys()))
        trait_map = annotations[trait]
        for k, v in trait_map.items():
            mapping[k] = str(v)
        return mapping

    # otherwise try to stringify
    for k, v in annotations.items():
        mapping[str(k)] = str(v)
    return mapping


def _match_label_for_video(mapping: Dict[str, str], video_name: str) -> Optional[str]:
    # Try exact filename
    if video_name in mapping:
        return mapping[video_name]
    # Try base name without extension
    stem = Path(video_name).stem
    if stem in mapping:
        return mapping[stem]
    # If vids like name.000.mp4, try part before first dot
    prefix = video_name.split(".")[0]
    if prefix in mapping:
        return mapping[prefix]
    # Try filename including extension
    if video_name in mapping:
        return mapping[video_name]
    return None


def extract_frames_from_video(
    video_path: Path,
    out_dir: Path,
    frames_per_second: float = 1.0,
    max_frames: Optional[int] = None,
    seed: int = 42,
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    if iio is None:
        raise RuntimeError("imageio (and imageio-ffmpeg) are required for video decoding. Install backend/ml_personality_pipeline/requirements.txt")

    try:
        reader = iio.get_reader(str(video_path))
    except Exception as exc:
        print(f"Failed to open {video_path}: {exc}")
        return saved_paths

    meta = {}
    try:
        meta = reader.get_meta_data()
    except Exception:
        meta = {}

    fps = meta.get("fps") or meta.get("fps", None)
    if fps is None:
        # fallback guess
        approx_fps = 30.0
    else:
        approx_fps = float(fps)

    step = max(1, int(round(approx_fps / max(0.0001, frames_per_second))))

    frame_idx = 0
    saved_count = 0
    try:
        for idx, frame in enumerate(reader):
            if idx % step != 0:
                continue
            # save
            out_name = f"{video_path.stem}_frame{frame_idx:05d}.jpg"
            out_path = out_dir / out_name
            try:
                # frame is a numpy array; use imageio.imwrite via iio
                iio.imwrite(str(out_path), frame)
                saved_paths.append(out_path)
                saved_count += 1
                frame_idx += 1
            except Exception:
                # skip corrupt frame
                continue
            if max_frames is not None and saved_count >= max_frames:
                break
    except Exception:
        # fallback: attempt reading with older iterator style
        try:
            for idx, frame in enumerate(iio.imiter(str(video_path))):
                if idx % step != 0:
                    continue
                out_name = f"{video_path.stem}_frame{frame_idx:05d}.jpg"
                out_path = out_dir / out_name
                try:
                    iio.imwrite(str(out_path), frame)
                    saved_paths.append(out_path)
                    saved_count += 1
                    frame_idx += 1
                except Exception:
                    continue
                if max_frames is not None and saved_count >= max_frames:
                    break
        except Exception as exc:
            print(f"Fallback extraction failed for {video_path}: {exc}")

    try:
        reader.close()
    except Exception:
        pass

    return saved_paths


def process_dataset(
    input_dir: Path,
    annotations_path: Path,
    out_root: Path,
    frames_dir_name: str = "frames",
    fps: float = 1.0,
    max_frames_per_video: Optional[int] = None,
    seed: int = 42,
    label_column: Optional[str] = None,
) -> dict:
    random.seed(seed)

    annotations = load_labels_from_csv_or_json(annotations_path)

    out_frames_root = out_root / frames_dir_name
    out_frames_root.mkdir(parents=True, exist_ok=True)

    video_paths = sorted([p for p in input_dir.rglob("*.mp4")])
    num_videos = len(video_paths)
    total_frames = 0
    written_rows = []
    missing_labels = 0
    class_counts: Dict[str, int] = {}

    for video_path in video_paths:
        video_name = video_path.name
        label = _match_label_for_video(annotations, video_name)
        if label is None:
            # attempt matching by prefix-based key
            label = _match_label_for_video(annotations, video_name)
        if label is None:
            missing_labels += 1
            # skip videos w/o labels
            continue

        # per-video output folder optional, but we place frames into out_frames_root directly
        saved = extract_frames_from_video(
            video_path=video_path,
            out_dir=out_frames_root,
            frames_per_second=fps,
            max_frames=max_frames_per_video,
            seed=seed,
        )

        for p in saved:
            written_rows.append((p.name, label))
            class_counts[label] = class_counts.get(label, 0) + 1
        total_frames += len(saved)

    # write labels.csv next to frames root
    labels_csv = out_root / "labels.csv"
    with labels_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["filename", "label"])
        for name, label in written_rows:
            writer.writerow([name, label])

    # save label encoder
    classes = sorted(class_counts.keys())
    label_map = {cls: idx for idx, cls in enumerate(classes)}
    labels_txt = out_root / "labels.txt"
    with labels_txt.open("w", encoding="utf-8") as handle:
        for cls, idx in label_map.items():
            handle.write(f"{idx}\t{cls}\n")

    summary = {
        "num_videos_found": num_videos,
        "num_videos_with_labels": num_videos - missing_labels,
        "num_frames_generated": total_frames,
        "num_classes": len(classes),
        "class_distribution": class_counts,
        "frames_root": str(out_frames_root),
        "labels_csv": str(labels_csv),
    }

    summary_path = out_root / "processing_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    # print stats
    print(f"Videos found: {num_videos}")
    print(f"Videos with labels: {num_videos - missing_labels}")
    print(f"Frames generated: {total_frames}")
    print("Class distribution:")
    for cls, cnt in sorted(class_counts.items(), key=lambda x: -x[1]):
        print(f"  {cls}: {cnt}")

    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process video dataset into image frames and labels CSV.")
    parser.add_argument("--input-dir", type=Path, default=None, help="Root folder containing videos (train/val/test).")
    parser.add_argument("--annotations", type=Path, required=True, help="Annotation file (CSV/JSON/pkl) mapping video->label.")
    parser.add_argument("--out-root", type=Path, default=None, help="Output root for processed dataset (default: pipeline/processed_dataset).")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames per second to extract (1.0 or 2.0 recommended).")
    parser.add_argument("--max-frames-per-video", type=int, default=None)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = DEFAULT_CONFIG
    input_dir = Path(args.input_dir) if args.input_dir is not None else config.dataset_root
    out_root = Path(args.out_root) if args.out_root is not None else Path(__file__).resolve().parent / "processed_dataset"
    process_dataset(
        input_dir=input_dir,
        annotations_path=Path(args.annotations),
        out_root=out_root,
        fps=args.fps,
        max_frames_per_video=args.max_frames_per_video,
        seed=args.seed,
    )
    print(f"Saved processed dataset to {out_root}")


if __name__ == "__main__":
    main()
