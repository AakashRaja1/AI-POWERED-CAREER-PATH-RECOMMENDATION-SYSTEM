"""
Training API. It exposes training-run status and history so the project can show how model training jobs are tracked from the backend.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.training_service import training_manager, TrainingStatus

router = APIRouter(prefix="/training", tags=["training"])


class TrainingStartRequest(BaseModel):
    """Request to start training"""
    name: Optional[str] = "Personality CNN Model"


class TrainingStatusResponse(BaseModel):
    """Training status response"""
    job_id: str
    status: str
    progress: float
    current_epoch: int
    total_epochs: int
    current_loss: float
    val_loss: float
    accuracy: float
    message: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


class TrainingStartResponse(BaseModel):
    """Response when training starts"""
    job_id: str
    status: str
    message: str


@router.post("/start", response_model=TrainingStartResponse)
async def start_training(request: TrainingStartRequest):
    """
    Start personality model training
    
    Returns: job_id to query training progress
    """
    try:
        job_id = str(uuid.uuid4())
        
        # Create job
        training_manager.create_job(job_id)
        
        # Start training in background
        training_manager.start_training(job_id)
        
        return TrainingStartResponse(
            job_id=job_id,
            status="pending",
            message=f"Training started! Job ID: {job_id}"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}", response_model=TrainingStatusResponse)
async def get_training_status(job_id: str):
    """
    Get current training status and progress
    
    Args: job_id from training start response
    Returns: Current training metrics and status
    """
    try:
        status = training_manager.get_job(job_id)
        
        if not status:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
        return TrainingStatusResponse(
            job_id=status.job_id,
            status=status.status,
            progress=status.progress,
            current_epoch=status.current_epoch,
            total_epochs=status.total_epochs,
            current_loss=status.current_loss,
            val_loss=status.val_loss,
            accuracy=status.accuracy,
            message=status.message,
            started_at=status.started_at,
            completed_at=status.completed_at,
            error=status.error
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs")
async def list_training_jobs():
    """List all training jobs (completed and in progress)"""
    try:
        jobs = []
        for status in training_manager.list_jobs():
            jobs.append({
                "job_id": status.job_id,
                "status": status.status,
                "progress": status.progress,
                "current_epoch": status.current_epoch,
                "total_epochs": status.total_epochs,
                "message": status.message,
                "started_at": status.started_at,
                "completed_at": status.completed_at
            })
        return {"jobs": jobs, "total": len(jobs)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def training_health():
    """Check if training service is healthy"""
    jobs = training_manager.list_jobs()
    return {
        "status": "healthy",
        "active_jobs": len([j for j in jobs if j.status == "running"]),
        "completed_jobs": len([j for j in jobs if j.status == "completed"])
    }
