from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import crud
from app.database.models import User, Prediction
from app.database.session import get_session
from app.api.routers.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

# Response models
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    is_admin: bool
    
    model_config = {"from_attributes": True}

class PredictionResponse(BaseModel):
    id: int
    user_id: int
    best_fit_career_domain: str
    confidence_score: float
    career_rationale: str
    growth_roadmap: str
    skill_gap_analysis: str
    recommended_courses: str
    backup_career_option: str
    behavioral_insight: str
    
    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None

class PredictionUpdate(BaseModel):
    best_fit_career_domain: Optional[str] = None
    confidence_score: Optional[float] = None
    career_rationale: Optional[str] = None
    growth_roadmap: Optional[str] = None
    skill_gap_analysis: Optional[str] = None
    recommended_courses: Optional[str] = None
    backup_career_option: Optional[str] = None
    behavioral_insight: Optional[str] = None

def require_admin(current_user: User = Depends(get_current_user)):
    """Check if current user is admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin)
):
    """Get all registered users"""
    users = crud.get_all_users(session)
    return [UserResponse(
        id=u.id,
        full_name=u.full_name,
        email=u.email,
        is_admin=u.is_admin
    ) for u in users]

@router.get("/predictions", response_model=List[PredictionResponse])
def get_all_predictions(
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin)
):
    """Get all predictions from all users"""
    predictions = crud.get_all_predictions(session)
    return [PredictionResponse(
        id=p.id,
        user_id=p.user_id,
        best_fit_career_domain=p.best_fit_career_domain,
        confidence_score=p.confidence_score,
        career_rationale=p.career_rationale,
        growth_roadmap=p.growth_roadmap,
        skill_gap_analysis=p.skill_gap_analysis,
        recommended_courses=p.recommended_courses,
        backup_career_option=p.backup_career_option,
        behavioral_insight=p.behavioral_insight
    ) for p in predictions]

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin)
):
    """Delete a user"""
    if crud.delete_user(session, user_id):
        return {"message": "User deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

@router.delete("/predictions/{prediction_id}")
def delete_prediction(
    prediction_id: int,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin)
):
    """Delete a prediction"""
    if crud.delete_prediction(session, prediction_id):
        return {"message": "Prediction deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Prediction not found"
    )

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin)
):
    """Update a user"""
    updated_user = crud.update_user(
        session,
        user_id,
        full_name=user_update.full_name,
        email=user_update.email
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(
        id=updated_user.id,
        full_name=updated_user.full_name,
        email=updated_user.email,
        is_admin=updated_user.is_admin
    )

@router.put("/predictions/{prediction_id}", response_model=PredictionResponse)
def update_prediction(
    prediction_id: int,
    prediction_update: PredictionUpdate,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin)
):
    """Update a prediction"""
    prediction = crud.get_prediction_by_id(session, prediction_id)
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )
    
    # Update fields if provided
    if prediction_update.best_fit_career_domain is not None:
        prediction.best_fit_career_domain = prediction_update.best_fit_career_domain
    if prediction_update.confidence_score is not None:
        prediction.confidence_score = prediction_update.confidence_score
    if prediction_update.career_rationale is not None:
        prediction.career_rationale = prediction_update.career_rationale
    if prediction_update.growth_roadmap is not None:
        prediction.growth_roadmap = prediction_update.growth_roadmap
    if prediction_update.skill_gap_analysis is not None:
        prediction.skill_gap_analysis = prediction_update.skill_gap_analysis
    if prediction_update.recommended_courses is not None:
        prediction.recommended_courses = prediction_update.recommended_courses
    if prediction_update.backup_career_option is not None:
        prediction.backup_career_option = prediction_update.backup_career_option
    if prediction_update.behavioral_insight is not None:
        prediction.behavioral_insight = prediction_update.behavioral_insight
    
    session.add(prediction)
    session.commit()
    session.refresh(prediction)
    
    return PredictionResponse(
        id=prediction.id,
        user_id=prediction.user_id,
        best_fit_career_domain=prediction.best_fit_career_domain,
        confidence_score=prediction.confidence_score,
        career_rationale=prediction.career_rationale,
        growth_roadmap=prediction.growth_roadmap,
        skill_gap_analysis=prediction.skill_gap_analysis,
        recommended_courses=prediction.recommended_courses,
        backup_career_option=prediction.backup_career_option,
        behavioral_insight=prediction.behavioral_insight
    )

