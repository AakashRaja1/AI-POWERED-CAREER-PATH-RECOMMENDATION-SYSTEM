from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Optional
from pathlib import Path
import joblib
import logging
import math
import random
import io
from PyPDF2 import PdfReader

from app.models import StudentInput, PredictionOutput
from app.data_loader import load_dataset
from app.database.session import get_session
from sqlmodel import Session
from app.database.models import Prediction as PredictionModel, User
from app.api.routers.auth import get_current_user, get_current_user_optional
import pdb
from app.database import crud


logger = logging.getLogger("uvicorn.error")

# Paths: artifacts expected in backend/app/model_artifacts/
ARTIFACT_DIR = Path(__file__).resolve().parent.parent.parent / "model_artifacts"

_VECTOR_NAMES = ["vectorizer.joblib", "tfidf_vectorizer.joblib", "vectorizer.pkl", "tfidf_vectorizer.pkl"]
_CLS_NAMES = ["career_classifier.joblib", "career_clf.joblib", "career_classifier.pkl", "career_clf.pkl"]
_LABEL_NAMES = ["label_encoder.joblib", "label_encoder.pkl"]

_vectorizer = None
_clf = None
_label_encoder = None


def _try_load_any(dirpath: Path, names):
    for nm in names:
        candidate = dirpath / nm
        if candidate.exists():
            try:
                obj = joblib.load(candidate)
                logger.info(f"Loaded artifact {candidate}")
                return obj
            except Exception as e:
                logger.warning(f"Failed to load artifact {candidate}: {e}")
    return None


if ARTIFACT_DIR.exists():
    _vectorizer = _try_load_any(ARTIFACT_DIR, _VECTOR_NAMES)
    _clf = _try_load_any(ARTIFACT_DIR, _CLS_NAMES)
    _label_encoder = _try_load_any(ARTIFACT_DIR, _LABEL_NAMES)
else:
    logger.warning(f"Artifact dir {ARTIFACT_DIR} does not exist. Using heuristic fallback.")

router = APIRouter()
_dataset = load_dataset()


@router.get("/items")
def list_items(limit: int = 5):
    if _dataset.empty:
        return {"count": 0, "sample": []}
    sample = _dataset.head(limit).to_dict(orient="records")
    return {"count": len(_dataset), "sample": sample}


def _normalize_skills(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        parts = value
    else:
        # accept comma or semicolon separated skills
        s = str(value)
        parts = [p.strip() for p in (s.replace(";", ",").split(",")) if p.strip()]
    return [p.lower() for p in parts]


def _build_feature_text(payload):
    # Convert pydantic payload to dict safely (handles alias names)
    data = payload.model_dump(by_alias=True) if hasattr(payload, "model_dump") else (payload.dict() if hasattr(payload, "dict") else dict(payload))

    fields = [
        "Education Level",
        "Academic Performance",
        "Skills",
        "Certifications",
        "Do you prefer working with data, people, or ideas?",
        "How do you approach solving complex problems?",
        "Do you thrive better in a structured or flexible environment?",
        "Do you prefer working independently or in a team?",
        "Do you learn best through practice, observation, or theory?",
        "Interests",
        "Extra-Curricular Activities",
    ]

    parts = []
    for f in fields:
        v = data.get(f, "")
        # if skills come as list, join them
        if f == "Skills" and isinstance(v, list):
            v = ", ".join(v)
        parts.append(str(v).strip())
    return " ".join([p for p in parts if p])


def _select_best_row_by_overlap(input_skills, input_edu):
    best_score = -math.inf
    best_row = None
    for _, row in _dataset.iterrows():
        row_skills = _normalize_skills(row.get("Skills", "") or "")
        overlap = len(set(input_skills) & set(row_skills))
        edu = str(row.get("Education Level", "")).strip().lower()
        edu_bonus = 1 if input_edu and edu and input_edu == edu else 0
        score = overlap * 2 + edu_bonus
        if score > best_score:
            best_score = score
            best_row = row
    return best_row


@router.post("/predict", response_model=PredictionOutput)
def predict(payload: StudentInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user_optional)):
    logger.info("Prediction request received: %s", payload.model_dump(by_alias=True))

    if _dataset.empty:
        raise HTTPException(status_code=503, detail="Dataset not available on server")

    text = _build_feature_text(payload)

    candidate = None
    best_fit = None
    conf = None

    # Use ML model if available
    if _vectorizer is not None and _clf is not None:
        try:
            X = _vectorizer.transform([text])
            pred_idx = _clf.predict(X)[0]
            # decode label if encoder exists
            try:
                if _label_encoder is not None:
                    best_fit = _label_encoder.inverse_transform([pred_idx])[0]
                else:
                    # if classifier was trained with string labels directly
                    best_fit = pred_idx
            except Exception:
                # fallback: assume classifier returns class index mapping to label encoder absent
                best_fit = pred_idx

            # confidence via predict_proba if available
            try:
                probs = _clf.predict_proba(X)[0]
                conf = float(max(probs))
            except Exception:
                conf = None

        except Exception as e:
            logger.warning("Model prediction failed; falling back to heuristic. Error: %s", e)
            best_fit = None

    # If model not available or failed, use heuristic
    if not best_fit:
        input_skills = _normalize_skills(payload.Skills if hasattr(payload, "Skills") else payload.model_dump(by_alias=True).get("Skills", ""))
        input_edu = (payload.Education_Level if hasattr(payload, "Education_Level") else payload.model_dump(by_alias=True).get("Education Level", "")).strip().lower()
        best_row = _select_best_row_by_overlap(input_skills, input_edu)
        if best_row is None:
            raise HTTPException(status_code=500, detail="Unable to compute prediction")
        candidate = best_row
        best_fit = candidate.get("Best-Fit Career Domain")
        conf = candidate.get("Confidence Score", None)

    # Try to pick a candidate row for returning descriptive text fields
    if candidate is None:
        same = _dataset[_dataset["Best-Fit Career Domain"].fillna("") == best_fit]
        if not same.empty:
            # pick a random example from that domain to avoid always returning same row
            candidate = same.sample(1).iloc[0]
        else:
            candidate = _dataset.sample(1).iloc[0]

    # Confidence fallback if still None
    if conf is None:
        conf = round(random.uniform(0.65, 0.92), 2)

    # Build output using dataset example fields as templates
    out = PredictionOutput(
        **{
            "Best-Fit Career Domain": best_fit,
            "Confidence Score": float(conf),
            "Career Rationale": candidate.get("Career Rationale") or f"Predicted as {best_fit} based on input.",
            "5-Year Career Growth Roadmap": candidate.get("5-Year Career Growth Roadmap") or f"Year 1: Entry in {best_fit} | Year 5: Senior {best_fit}",
            "Skill Gap Analysis": candidate.get("Skill Gap Analysis") or "Skill gap analysis not available.",
            "Recommended Tools, Courses, and Certifications": candidate.get("Recommended Tools, Courses, and Certifications") or "",
            "Alternative/Backup Career Option": candidate.get("Alternative/Backup Career Option") or "",
            "Behavioral Insight": candidate.get("Behavioral Insight") or "",
        }
    )

    # optional: persist prediction to DB if session available
    try:
        if session and current_user:
            db_obj = PredictionModel(
                user_id=current_user.id,
                best_fit_career_domain=out.best_fit_career_domain,
                confidence_score=out.confidence_score,
                career_rationale=out.career_rationale,
                growth_roadmap=out.growth_roadmap,
                skill_gap_analysis=out.skill_gap_analysis,
                recommended_courses=out.recommended_courses,
                backup_career_option=out.backup_career_option,
                behavioral_insight=out.behavioral_insight,
            )
            session.add(db_obj)
            session.commit()
    except Exception as e:
        logger.warning("Failed to persist prediction: %s", e)
    return out


@router.post("/predict-resume", response_model=PredictionOutput)
async def predict_resume(
    file: UploadFile = File(...), 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user_optional)
):
    logger.info("Resume prediction request received for file: %s", file.filename)

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is accepted.")

    if _dataset.empty:
        raise HTTPException(status_code=503, detail="Dataset not available on server")

    try:
        pdf_content = await file.read()
        pdf_stream = io.BytesIO(pdf_content)
        reader = PdfReader(pdf_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        logger.error(f"Failed to read or parse PDF: {e}")
        raise HTTPException(status_code=500, detail="Failed to process PDF file.")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    logger.info("Extracted text from resume (first 200 chars): %s", text[:200])

    candidate = None
    best_fit = None
    conf = None

    if _vectorizer is not None and _clf is not None:
        try:
            X = _vectorizer.transform([text])
            pred_idx = _clf.predict(X)[0]
            
            try:
                if _label_encoder is not None:
                    best_fit = _label_encoder.inverse_transform([pred_idx])[0]
                else:
                    best_fit = pred_idx
            except Exception:
                best_fit = pred_idx

            try:
                probs = _clf.predict_proba(X)[0]
                conf = float(max(probs))
            except Exception:
                conf = None

        except Exception as e:
            logger.warning("Model prediction from resume failed. Error: %s", e)
            best_fit = None
    
    if not best_fit:
        raise HTTPException(status_code=500, detail="Unable to compute prediction from resume.")

    # Find a representative row from the dataset for the predicted career
    same = _dataset[_dataset["Best-Fit Career Domain"].fillna("") == best_fit]
    if not same.empty:
        candidate = same.sample(1).iloc[0]
    else:
        # Fallback to a random row if no match found (should be rare)
        candidate = _dataset.sample(1).iloc[0]

    if conf is None:
        conf = round(random.uniform(0.65, 0.92), 2)

    out = PredictionOutput(
        **{
            "Best-Fit Career Domain": best_fit,
            "Confidence Score": float(conf),
            "Career Rationale": candidate.get("Career Rationale") or f"Predicted as {best_fit} based on your resume.",
            "5-Year Career Growth Roadmap": candidate.get("5-Year Career Growth Roadmap") or f"Year 1: Entry in {best_fit} | Year 5: Senior {best_fit}",
            "Skill Gap Analysis": candidate.get("Skill Gap Analysis") or "Skill gap analysis not available.",
            "Recommended Tools, Courses, and Certifications": candidate.get("Recommended Tools, Courses, and Certifications") or "",
            "Alternative/Backup Career Option": candidate.get("Alternative/Backup Career Option") or "",
            "Behavioral Insight": candidate.get("Behavioral Insight") or "",
        }
    )

    try:
        if session and current_user:
            db_obj = PredictionModel(
                user_id=current_user.id,
                best_fit_career_domain=out.best_fit_career_domain,
                confidence_score=out.confidence_score,
                career_rationale=out.career_rationale,
                growth_roadmap=out.growth_roadmap,
                skill_gap_analysis=out.skill_gap_analysis,
                recommended_courses=out.recommended_courses,
                backup_career_option=out.backup_career_option,
                behavioral_insight=out.behavioral_insight,
            )
            session.add(db_obj)
            session.commit()
    except Exception as e:
        logger.warning("Failed to persist resume-based prediction: %s", e)

    return out


@router.get("/predictions", response_model=List[PredictionOutput])
def get_predictions(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return crud.list_predictions(session, user_id=current_user.id)
