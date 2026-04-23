from __future__ import annotations

import argparse
from pathlib import Path

import torch

try:
    from .config import DEFAULT_CONFIG, TRAIT_ORDER
    from .dataset_loader import VIDEO_EXTENSIONS, load_media, load_media_frames
    from .derived_traits import derive_personality_scores, describe_scores
    from .feature_extractor import ResNet18FeatureExtractor
    from .preprocessing import build_transforms
    from .utils import build_model_from_checkpoint, clamp_traits, load_checkpoint
except ImportError:
    from config import DEFAULT_CONFIG, TRAIT_ORDER
    from dataset_loader import VIDEO_EXTENSIONS, load_media, load_media_frames
    from derived_traits import derive_personality_scores, describe_scores
    from feature_extractor import ResNet18FeatureExtractor
    from preprocessing import build_transforms
    from utils import build_model_from_checkpoint, clamp_traits, load_checkpoint


class PersonalityPredictor:
    def __init__(self, model_path: str | Path = DEFAULT_CONFIG.model_path) -> None:
        model_path = Path(model_path)
        self.feature_extractor = ResNet18FeatureExtractor().to("cpu")
        self.model = build_model_from_checkpoint(model_path, input_dim=self.feature_extractor.feature_dim)
        self.transform = build_transforms(training=False)
        self.video_frames = max(1, int(DEFAULT_CONFIG.inference_video_frames))
        checkpoint = load_checkpoint(model_path)
        metadata = checkpoint.get("metadata", {})
        self.trait_order = tuple(checkpoint.get("trait_order") or metadata.get("trait_order") or TRAIT_ORDER)

    def predict(self, media_path: str | Path) -> dict[str, float]:
        path = Path(media_path)
        if not path.exists():
            raise FileNotFoundError(f"Media file not found: {path}")

        image = load_media(path)
        tensor = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            features = self.feature_extractor(tensor)
            values = self.model(features).squeeze(0).tolist()

        clipped_values = clamp_traits(values)
        return {trait: clipped_values[index] for index, trait in enumerate(self.trait_order)}

    def predict_enriched(self, media_path: str | Path) -> dict:
        path = Path(media_path)
        if not path.exists():
            raise FileNotFoundError(f"Media file not found: {path}")

        if path.suffix.lower() in VIDEO_EXTENSIONS:
            frames = load_media_frames(path, max_frames=self.video_frames)
        else:
            frames = [load_media(path)]

        tensors = torch.stack([self.transform(image) for image in frames], dim=0)

        with torch.no_grad():
            features = self.feature_extractor(tensors)
            values_per_frame = self.model(features)
            averaged_values = values_per_frame.mean(dim=0).tolist()
            variability_values = values_per_frame.std(dim=0, unbiased=False).tolist()

        all_traits = {
            trait: score
            for trait, score in zip(self.trait_order, clamp_traits(averaged_values))
        }
        base_traits = {trait: all_traits[trait] for trait in TRAIT_ORDER if trait in all_traits}
        direct_extra_traits = {trait: score for trait, score in all_traits.items() if trait not in TRAIT_ORDER}
        derived_scores = derive_personality_scores(base_traits)
        trait_variability = {
            trait: clamp_traits([score])[0]
            for trait, score in zip(self.trait_order, variability_values)
        }

        return {
            "traits": base_traits,
            "direct_traits": direct_extra_traits,
            "derived_scores": derived_scores,
            "score_levels": describe_scores(derived_scores),
            "meta": {
                "source_type": "video" if path.suffix.lower() in VIDEO_EXTENSIONS else "image",
                "frames_used": len(frames),
                "trait_order": list(self.trait_order),
                "trait_variability": trait_variability,
                "derived_note": "Derived scores are heuristic composites based on Big Five outputs.",
            },
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run personality inference on an image or video.")
    parser.add_argument("media_path", type=str, help="Path to an image or MP4 file.")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_CONFIG.model_path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    predictor = PersonalityPredictor(model_path=args.model_path)
    prediction = predictor.predict(args.media_path)
    for trait, score in prediction.items():
        print(f"{trait}: {score:.4f}")


if __name__ == "__main__":
    main()
