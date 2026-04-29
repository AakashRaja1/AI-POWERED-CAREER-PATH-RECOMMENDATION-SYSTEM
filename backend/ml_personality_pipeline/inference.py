from __future__ import annotations

import argparse
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np
import torch

try:
    import cv2
except Exception:  # pragma: no cover - optional dependency
    cv2 = None

try:
    import imageio_ffmpeg
except Exception:  # pragma: no cover - optional dependency
    imageio_ffmpeg = None

try:
    from .cnn_model import SimplePersonalityCNN
    from .config import DEFAULT_CONFIG, TRAIT_ORDER
    from .dataset_loader import VIDEO_EXTENSIONS, load_media, load_media_frames
    from .derived_traits import derive_personality_scores, describe_scores
    from .feature_extractor import ResNet18FeatureExtractor
    from .preprocessing import build_transforms
    from .utils import build_model_from_checkpoint, clamp_traits, load_checkpoint
except ImportError:
    from cnn_model import SimplePersonalityCNN
    from config import DEFAULT_CONFIG, TRAIT_ORDER
    from dataset_loader import VIDEO_EXTENSIONS, load_media, load_media_frames
    from derived_traits import derive_personality_scores, describe_scores
    from feature_extractor import ResNet18FeatureExtractor
    from preprocessing import build_transforms
    from utils import build_model_from_checkpoint, clamp_traits, load_checkpoint


class PersonalityPredictor:
    def __init__(self, model_path: str | Path = DEFAULT_CONFIG.model_path) -> None:
        model_path = Path(model_path)
        checkpoint = load_checkpoint(model_path)
        metadata = checkpoint.get("metadata", {})
        self.architecture = str(metadata.get("architecture", "feature_mlp"))
        self.trait_order = tuple(checkpoint.get("trait_order") or metadata.get("trait_order") or TRAIT_ORDER)
        self.transform = build_transforms(training=False)
        self.video_frames = max(1, int(DEFAULT_CONFIG.inference_video_frames))

        if self.architecture == "simple_cnn":
            self.feature_extractor = None
            self.model = SimplePersonalityCNN(
                output_dim=int(metadata.get("output_dim", len(self.trait_order))),
                dropout=0.0,
            ).to("cpu")
            self.model.load_state_dict(checkpoint["model_state_dict"])
            self.model.eval()
        else:
            self.feature_extractor = ResNet18FeatureExtractor().to("cpu")
            self.model = build_model_from_checkpoint(model_path, input_dim=self.feature_extractor.feature_dim)

    def _detect_faces(self, image) -> list[tuple[int, int, int, int]]:
        if cv2 is None:
            return []

        array = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
        cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(str(cascade_path))
        faces = detector.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=4, minSize=(32, 32))
        return [tuple(int(v) for v in face) for face in faces]

    def _smile_detected(self, image, face: tuple[int, int, int, int]) -> bool:
        if cv2 is None:
            return False

        array = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
        cascade_path = Path(cv2.data.haarcascades) / "haarcascade_smile.xml"
        detector = cv2.CascadeClassifier(str(cascade_path))
        x, y, w, h = face
        face_roi = gray[y : y + h, x : x + w]
        if face_roi.size == 0:
            return False
        smiles = detector.detectMultiScale(face_roi, scaleFactor=1.7, minNeighbors=20, minSize=(20, 20))
        return len(smiles) > 0

    def _analyze_frames(self, frames, source_type: str) -> dict:
        face_rows = []
        smile_count = 0

        for image in frames:
            width, height = image.size
            faces = self._detect_faces(image)
            if not faces:
                face_rows.append({"detected": False})
                continue

            largest = max(faces, key=lambda item: item[2] * item[3])
            x, y, w, h = largest
            center_x = (x + w / 2) / max(1.0, width)
            center_y = (y + h / 2) / max(1.0, height)
            face_area = (w * h) / max(1.0, width * height)
            centeredness = 1.0 - min(1.0, (((center_x - 0.5) ** 2 + (center_y - 0.45) ** 2) ** 0.5) / 0.7)
            smiling = self._smile_detected(image, largest)
            smile_count += 1 if smiling else 0
            face_rows.append(
                {
                    "detected": True,
                    "center_x": center_x,
                    "center_y": center_y,
                    "face_area": face_area,
                    "centeredness": centeredness,
                    "smiling": smiling,
                }
            )

        detected_rows = [row for row in face_rows if row.get("detected")]
        detection_rate = len(detected_rows) / max(1, len(face_rows))

        if source_type == "image" and detection_rate == 0:
            raise ValueError("No person/face detected in the image. Please upload a clear image where the person is inside the frame.")
        if source_type == "video" and detection_rate < 0.25:
            raise ValueError("No person/face detected clearly in the video frames. Please upload a video where the person stays visible in the frame.")

        face_area_values = [row["face_area"] for row in detected_rows]
        centered_values = [row["centeredness"] for row in detected_rows]
        centers = [(row["center_x"], row["center_y"]) for row in detected_rows]
        movement = 0.0
        if len(centers) > 1:
            distances = [
                ((centers[index][0] - centers[index - 1][0]) ** 2 + (centers[index][1] - centers[index - 1][1]) ** 2) ** 0.5
                for index in range(1, len(centers))
            ]
            movement = float(np.mean(distances))

        expression_score = smile_count / max(1, len(detected_rows))
        face_area_std = float(np.std(face_area_values or [0.0]))
        centering_std = float(np.std(centered_values or [0.0]))
        stability_score = max(0.0, min(1.0, 1.0 - (movement * 8.0 + centering_std)))
        engagement_score = min(
            1.0,
            0.45 * detection_rate
            + 0.25 * float(np.mean(centered_values or [0.0]))
            + 0.20 * min(1.0, float(np.mean(face_area_values or [0.0])) * 8.0)
            + 0.10 * min(1.0, movement * 10.0),
        )
        if detection_rate >= 0.85:
            presence_quality = "strong"
        elif detection_rate >= 0.55:
            presence_quality = "partial"
        else:
            presence_quality = "weak"

        if expression_score >= 0.55:
            expression_pattern = "frequent positive expression"
        elif expression_score >= 0.20:
            expression_pattern = "some positive expression"
        else:
            expression_pattern = "neutral or limited visible expression"

        return {
            "person_detected": True,
            "face_detection_rate": round(detection_rate, 3),
            "frames_with_face": len(detected_rows),
            "average_face_area": round(float(np.mean(face_area_values or [0.0])), 4),
            "face_area_variability": round(face_area_std, 4),
            "face_centering_score": round(float(np.mean(centered_values or [0.0])), 3),
            "face_centering_variability": round(centering_std, 3),
            "expression_smile_rate": round(expression_score, 3),
            "expression_pattern": expression_pattern,
            "head_motion_score": round(min(1.0, movement * 10.0), 3),
            "posture_stability_score": round(stability_score, 3),
            "visual_engagement_score": round(engagement_score, 3),
            "presence_quality": presence_quality,
        }

    def _analyze_audio(self, path: Path) -> dict:
        if imageio_ffmpeg is None:
            return {"voice_available": False, "reason": "imageio-ffmpeg is not installed"}

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio_path = Path(temp_audio.name)

        try:
            command = [
                imageio_ffmpeg.get_ffmpeg_exe(),
                "-y",
                "-i",
                str(path),
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-sample_fmt",
                "s16",
                str(audio_path),
            ]
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
            if result.returncode != 0 or not audio_path.exists() or audio_path.stat().st_size == 0:
                return {"voice_available": False, "reason": "No readable audio track found"}

            with wave.open(str(audio_path), "rb") as wav:
                sample_rate = wav.getframerate()
                frames = wav.readframes(wav.getnframes())
            samples = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
            if samples.size == 0:
                return {"voice_available": False, "reason": "Audio track is empty"}

            samples = samples / 32768.0
            window = max(1, int(sample_rate * 0.15))
            energies = [
                float(np.sqrt(np.mean(samples[index : index + window] ** 2)))
                for index in range(0, len(samples), window)
                if samples[index : index + window].size
            ]
            if not energies:
                return {"voice_available": False, "reason": "Audio energy could not be measured"}

            noise_floor = float(np.percentile(energies, 25))
            threshold = max(0.015, noise_floor * 2.5)
            active = [energy for energy in energies if energy >= threshold]
            activity_ratio = len(active) / max(1, len(energies))
            energy_variability = float(np.std(energies))
            transitions = sum(
                1
                for index in range(1, len(energies))
                if (energies[index] >= threshold) != (energies[index - 1] >= threshold)
            )
            pause_ratio = 1.0 - activity_ratio
            rhythm_score = min(1.0, transitions / max(1, len(energies) - 1))
            if activity_ratio >= 0.55:
                pattern = "active speaking"
            elif activity_ratio >= 0.20:
                pattern = "some speaking"
            else:
                pattern = "little or no speaking"

            return {
                "voice_available": True,
                "speaking_activity_ratio": round(activity_ratio, 3),
                "pause_ratio": round(pause_ratio, 3),
                "voice_energy": round(float(np.mean(energies)), 4),
                "voice_variability": round(energy_variability, 4),
                "speech_rhythm_score": round(rhythm_score, 3),
                "talking_pattern": pattern,
            }
        except Exception as error:
            return {"voice_available": False, "reason": str(error)}
        finally:
            audio_path.unlink(missing_ok=True)

    def predict(self, media_path: str | Path) -> dict[str, float]:
        path = Path(media_path)
        if not path.exists():
            raise FileNotFoundError(f"Media file not found: {path}")

        image = load_media(path)
        tensor = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            if self.feature_extractor is None:
                values = self.model(tensor).squeeze(0).tolist()
            else:
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
            source_type = "video"
        else:
            frames = [load_media(path)]
            source_type = "image"

        frame_analysis = self._analyze_frames(frames, source_type=source_type)
        audio_analysis = self._analyze_audio(path) if source_type == "video" else {
            "voice_available": False,
            "reason": "Audio analysis applies to video uploads only",
        }

        tensors = torch.stack([self.transform(image) for image in frames], dim=0)

        with torch.no_grad():
            if self.feature_extractor is None:
                values_per_frame = self.model(tensors)
            else:
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
        reliability_score = min(
            1.0,
            0.55 * frame_analysis.get("face_detection_rate", 0.0)
            + 0.25 * frame_analysis.get("face_centering_score", 0.0)
            + 0.20 * (1.0 - min(1.0, float(np.mean(list(trait_variability.values()) or [0.0])) * 20.0)),
        )
        behavior_summary = (
            f"Person visibility is {frame_analysis.get('presence_quality', 'unknown')}; "
            f"expression pattern is {frame_analysis.get('expression_pattern', 'unknown')}; "
            f"talking pattern is {audio_analysis.get('talking_pattern', audio_analysis.get('reason', 'not available'))}."
        )

        return {
            "traits": base_traits,
            "direct_traits": direct_extra_traits,
            "derived_scores": derived_scores,
            "score_levels": describe_scores(derived_scores),
            "behavior_analysis": {
                "frame_analysis": frame_analysis,
                "audio_analysis": audio_analysis,
                "reliability_score": round(reliability_score, 3),
                "behavior_summary": behavior_summary,
                "video_note": "Video behavior analysis combines sampled frame predictions, face presence, expression cues, head movement, and audio activity when available.",
            },
            "meta": {
                "source_type": source_type,
                "frames_used": len(frames),
                "trait_order": list(self.trait_order),
                "model_architecture": self.architecture,
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
