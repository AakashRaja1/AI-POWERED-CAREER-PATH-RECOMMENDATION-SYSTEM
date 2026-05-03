"""
Personality pipeline module. It supports data preparation, model training, evaluation, or inference for behavior-based career guidance. This file handles the train video model part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from video_training import build_config, train_video_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the v2 First Impressions video model.")
    parser.add_argument("--config", type=Path, default=Path("config/video_training.yaml"), help="Path to the YAML training config.")
    parser.add_argument("--debug", action="store_true", help="Print sample predictions after evaluation.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = build_config(args.config)
    if args.debug:
        config = type(config)(**{**config.__dict__, "debug": True})
    metrics = train_video_model(config)
    print(f"Saved v2 model to {metrics['summary']['best_model_path']}")
    print(f"Saved metrics to {config.metrics_path}")


if __name__ == "__main__":
    main()
