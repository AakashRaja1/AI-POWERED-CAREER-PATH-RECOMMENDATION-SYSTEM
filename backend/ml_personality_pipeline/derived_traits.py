"""
Derived trait calculator. It turns raw model outputs into extra human-readable behavior indicators used in the result screens.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

from typing import Dict


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def score_bucket(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "moderate"
    return "low"


def derive_personality_scores(base_traits: Dict[str, float]) -> Dict[str, float]:
    openness = _clamp(base_traits.get("openness", 0.0))
    conscientiousness = _clamp(base_traits.get("conscientiousness", 0.0))
    extraversion = _clamp(base_traits.get("extraversion", 0.0))
    agreeableness = _clamp(base_traits.get("agreeableness", 0.0))
    neuroticism = _clamp(base_traits.get("neuroticism", 0.0))

    emotional_stability = _clamp(1.0 - neuroticism)

    # These are calibrated heuristic composites derived from Big Five outputs.
    derived = {
        "extrovert_score": _clamp(extraversion),
        "introvert_score": _clamp(1.0 - extraversion),
        "confidence_score": _clamp(
            0.55 * extraversion + 0.30 * emotional_stability + 0.15 * conscientiousness
        ),
        "professionalism_score": _clamp(
            0.40 * conscientiousness + 0.25 * agreeableness + 0.20 * emotional_stability + 0.15 * openness
        ),
        "leadership_potential": _clamp(
            0.35 * extraversion + 0.30 * conscientiousness + 0.20 * openness + 0.15 * emotional_stability
        ),
        "teamwork_score": _clamp(
            0.45 * agreeableness + 0.25 * extraversion + 0.20 * conscientiousness + 0.10 * emotional_stability
        ),
        "communication_score": _clamp(
            0.60 * extraversion + 0.25 * agreeableness + 0.15 * openness
        ),
        "emotional_stability": emotional_stability,
        "curiosity_learning_score": _clamp(0.70 * openness + 0.30 * conscientiousness),
    }
    return derived


def describe_scores(scores: Dict[str, float]) -> Dict[str, str]:
    return {name: score_bucket(value) for name, value in scores.items()}
