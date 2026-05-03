from __future__ import annotations

import json
import re
import shutil
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from chatbot.groq_client import get_groq_client
from app.core.config import settings
from ml_personality_pipeline.inference import PersonalityPredictor


router = APIRouter(prefix="/personality", tags=["personality"])
_LLM_EXECUTOR = ThreadPoolExecutor(max_workers=4)

_ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".mp4", ".mov", ".avi", ".mkv", ".webm"}

# Use the checkpoint produced by the standalone personality training flow.
_MODEL_PATH = Path(__file__).resolve().parents[3] / "ml_personality_pipeline" / "artifacts" / "personality_model.pth"


try:
    _predictor = PersonalityPredictor(model_path=_MODEL_PATH)
except Exception:
    _predictor = None


class CareerRecommendationRequest(BaseModel):
    personality_score: Dict[str, Any] = Field(default_factory=dict)
    questionnaire_responses: Dict[str, str] = Field(default_factory=dict)
    additional_notes: str = ""


def _format_personality_payload(payload: Dict[str, Any]) -> str:
    traits = payload.get("traits") or {}
    direct_traits = payload.get("direct_traits") or {}
    derived_scores = payload.get("derived_scores") or {}
    score_levels = payload.get("score_levels") or {}
    meta = payload.get("meta") or {}

    lines: List[str] = ["PERSONALITY SCORE SUMMARY:"]

    if traits:
        lines.append("- Big Five traits:")
        for key, value in traits.items():
            lines.append(f"  - {key}: {value}")

    if direct_traits:
        lines.append("- Direct traits:")
        for key, value in direct_traits.items():
            lines.append(f"  - {key}: {value}")

    if derived_scores:
        lines.append("- Derived scores:")
        for key, value in derived_scores.items():
            level = score_levels.get(key)
            suffix = f" ({level})" if level else ""
            lines.append(f"  - {key}: {value}{suffix}")

    if meta:
        lines.append("- Meta:")
        for key, value in meta.items():
            lines.append(f"  - {key}: {value}")

    return "\n".join(lines)


def _format_questionnaire_responses(responses: Dict[str, str]) -> str:
    lines = ["CAREER QUESTIONNAIRE RESPONSES:"]
    for key, value in responses.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def _extract_json_payload(raw_content: str) -> Dict[str, Any] | None:
    content = (raw_content or "").strip()
    if not content:
        return None

    try:
        data = json.loads(content)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", content, flags=re.IGNORECASE)
    if fenced:
        try:
            data = json.loads(fenced.group(1))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = content[start : end + 1]
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            return None

    return None


def _normalize_recommendation(parsed: Dict[str, Any] | None, fallback_text: str) -> Dict[str, Any]:
    parsed = parsed or {}

    def _as_list(value: Any) -> List[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [part.strip() for part in re.split(r"[,\n;]", value) if part.strip()]
        return []

    try:
        confidence_raw = parsed.get("confidence", 0.0)
        confidence = max(0.0, min(1.0, float(confidence_raw)))
    except (TypeError, ValueError):
        confidence = 0.0

    rationale = str(parsed.get("rationale", "")).strip() or fallback_text

    return {
        "career_path": str(parsed.get("career_path", "")).strip() or "Career recommendation",
        "rationale": rationale,
        "best_fit_roles": _as_list(parsed.get("best_fit_roles")),
        "skills_to_build": _as_list(parsed.get("skills_to_build")),
        "roadmap": _as_list(parsed.get("roadmap")),
        "confidence": confidence,
    }


def _call_recommendation_model(client, system_prompt: str, user_prompt: str):
    return client.chat.completions.create(
        model=settings.GROQ_CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=settings.GROQ_MAX_COMPLETION_TOKENS,
        temperature=0.2,
    )


@router.get("/health")
def health() -> dict:
    return {
        "status": "ok" if _predictor is not None else "model_unavailable",
        "model_path": str(_MODEL_PATH),
        "model_loaded": _predictor is not None,
    }


@router.post("/predict")
async def predict_personality(file: UploadFile = File(...)) -> dict:
    if _predictor is None:
        raise HTTPException(
            status_code=503,
            detail=f"Personality model is not loaded. Expected checkpoint at: {_MODEL_PATH}",
        )

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload an image or video file.",
        )

    tmp_path: Path | None = None
    try:
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = Path(tmp.name)
            await file.seek(0)
            shutil.copyfileobj(file.file, tmp)

        prediction = _predictor.predict_enriched(tmp_path)
        return prediction
    except HTTPException:
        raise
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Failed to run personality inference: {error}")
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        await file.close()


@router.post("/recommend-career")
async def recommend_career(req: CareerRecommendationRequest) -> dict:
    try:
        client = get_groq_client()
        personality_context = _format_personality_payload(req.personality_score)
        questionnaire_context = _format_questionnaire_responses(req.questionnaire_responses)
        additional_notes = req.additional_notes.strip() or "None"

        system_prompt = (
            "You are an expert career counselor. Recommend the best career based on personality and questionnaire answers. "
            "Be concise and practical. Return ONLY valid JSON with these keys: "
            "career_path (string), best_fit_roles (array of 3 role names), rationale (1-2 sentences), skills_to_build (array of 5 skills), "
            "roadmap (array of 3-4 short action steps), confidence (0-1 float). Be brief."
        )

        user_prompt = (
            f"{personality_context}\n\n"
            f"{questionnaire_context}\n\n"
            f"ADDITIONAL NOTES:\n{additional_notes}\n\n"
            "Give the single best-fit career path first, then explain why it matches the user."
        )

        future = _LLM_EXECUTOR.submit(_call_recommendation_model, client, system_prompt, user_prompt)
        response = future.result(timeout=settings.GROQ_REQUEST_TIMEOUT_SECONDS)

        raw_content = response.choices[0].message.content or ""
        parsed = _extract_json_payload(raw_content)
        recommendation = _normalize_recommendation(parsed, raw_content)

        return {
            "recommendation": recommendation,
            "raw_response": raw_content,
        }
    except FuturesTimeoutError:
        fallback = {
            "career_path": "Career recommendation pending",
            "rationale": "The recommendation service timed out. Please retry with shorter notes or fewer questionnaire fields.",
            "best_fit_roles": [],
            "skills_to_build": [],
            "roadmap": ["Retry request", "Use shorter input", "Review top matching roles"],
            "confidence": 0.0,
        }
        return {
            "recommendation": fallback,
            "raw_response": "",
        }
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate career recommendation: {e}")
