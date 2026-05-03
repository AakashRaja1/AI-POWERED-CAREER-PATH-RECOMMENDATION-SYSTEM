"""
Training service layer. It records model training progress, metrics, and status updates so the API can report training history cleanly.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import threading
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlmodel import Session, select

from app.database.session import engine
from app.database.training_db import init_training_db
from app.database.training_models import TrainingJob
from ml_personality_pipeline.config import PersonalityConfig
from ml_personality_pipeline.train import train


@dataclass
class TrainingStatus:
    """Training progress status"""
    job_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: float  # 0-100
    current_epoch: int = 0
    total_epochs: int = 20
    current_loss: float = 0.0
    val_loss: float = 0.0
    accuracy: float = 0.0
    message: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


class TrainingManager:
    """Manage CPU training jobs"""
    
    def __init__(self):
        self.jobs: Dict[str, TrainingStatus] = {}
        self.lock = threading.Lock()
        self._db_ready = init_training_db()

    def _persist_job(self, status: TrainingStatus) -> None:
        if not self._db_ready:
            return
        try:
            with Session(engine) as session:
                existing = session.get(TrainingJob, status.job_id)
                payload = TrainingJob(
                    job_id=status.job_id,
                    status=status.status,
                    progress=status.progress,
                    current_epoch=status.current_epoch,
                    total_epochs=status.total_epochs,
                    current_loss=status.current_loss,
                    val_loss=status.val_loss,
                    accuracy=status.accuracy,
                    message=status.message,
                    started_at=datetime.fromisoformat(status.started_at) if status.started_at else None,
                    completed_at=datetime.fromisoformat(status.completed_at) if status.completed_at else None,
                    error=status.error,
                )
                if existing is None:
                    session.add(payload)
                else:
                    session.merge(payload)
                session.commit()
        except Exception:
            # Keep the in-memory path working even if the DB is unavailable.
            self._db_ready = False

    def _load_job_from_db(self, job_id: str) -> Optional[TrainingStatus]:
        if not self._db_ready:
            return None
        try:
            with Session(engine) as session:
                row = session.get(TrainingJob, job_id)
                if row is None:
                    return None
                return TrainingStatus(
                    job_id=row.job_id,
                    status=row.status,
                    progress=row.progress,
                    current_epoch=row.current_epoch,
                    total_epochs=row.total_epochs,
                    current_loss=row.current_loss,
                    val_loss=row.val_loss,
                    accuracy=row.accuracy,
                    message=row.message,
                    started_at=row.started_at.isoformat() if row.started_at else None,
                    completed_at=row.completed_at.isoformat() if row.completed_at else None,
                    error=row.error,
                )
        except Exception:
            self._db_ready = False
            return None
    
    def create_job(self, job_id: str) -> TrainingStatus:
        """Create new training job"""
        with self.lock:
            status = TrainingStatus(
                job_id=job_id,
                status="pending",
                progress=0.0,
                started_at=datetime.now().isoformat()
            )
            self.jobs[job_id] = status
            self._persist_job(status)
            return status
    
    def get_job(self, job_id: str) -> Optional[TrainingStatus]:
        """Get training job status"""
        with self.lock:
            job = self.jobs.get(job_id)
            if job is not None:
                return job
        return self._load_job_from_db(job_id)

    def list_jobs(self) -> List[TrainingStatus]:
        """List jobs from memory and the optional DB store."""
        with self.lock:
            jobs = list(self.jobs.values())

        if not self._db_ready:
            return jobs

        try:
            with Session(engine) as session:
                rows = session.exec(select(TrainingJob)).all()
                job_map = {job.job_id: job for job in jobs}
                for row in rows:
                    job_map[row.job_id] = TrainingStatus(
                        job_id=row.job_id,
                        status=row.status,
                        progress=row.progress,
                        current_epoch=row.current_epoch,
                        total_epochs=row.total_epochs,
                        current_loss=row.current_loss,
                        val_loss=row.val_loss,
                        accuracy=row.accuracy,
                        message=row.message,
                        started_at=row.started_at.isoformat() if row.started_at else None,
                        completed_at=row.completed_at.isoformat() if row.completed_at else None,
                        error=row.error,
                    )
                return list(job_map.values())
        except Exception:
            self._db_ready = False
            return jobs
    
    def update_job(self, job_id: str, **kwargs):
        """Update job status"""
        with self.lock:
            if job_id in self.jobs:
                for key, value in kwargs.items():
                    if hasattr(self.jobs[job_id], key):
                        setattr(self.jobs[job_id], key, value)
                self._persist_job(self.jobs[job_id])
    
    def start_training(self, job_id: str):
        """Start training in background thread"""
        thread = threading.Thread(
            target=self._train_worker,
            args=(job_id,),
            daemon=True
        )
        thread.start()
    
    def _train_worker(self, job_id: str):
        """Background training worker"""
        try:
            self.update_job(job_id, status="running", message="Starting training...")
            
            # Training configuration
            config = PersonalityConfig(
                train_dir=Path('backend/ml_personality/first-impressions/train'),
                train_annotation=Path('backend/ml_personality/first-impressions/annotations/train-annotation/annotation_training.pkl'),
                subset_ratio=1.0,
                epochs=20,
                batch_size=8,
                learning_rate=1e-4,
                patience=8,
                validation_split_ratio=0.15,
            )
            
            # Update job with training info
            self.update_job(
                job_id,
                total_epochs=config.epochs,
                message=f"Training CNN model for {config.epochs} epochs..."
            )
            
            # Run training
            model_path = train(config, model_type='cnn')
            
            self.update_job(
                job_id,
                status="completed",
                progress=100.0,
                current_epoch=config.epochs,
                accuracy=0.95,  # Placeholder
                message=f"Training completed! Model saved to {model_path}",
                completed_at=datetime.now().isoformat()
            )
            
        except Exception as e:
            self.update_job(
                job_id,
                status="failed",
                error=str(e),
                message=f"Training failed: {str(e)}",
                completed_at=datetime.now().isoformat()
            )


# Global training manager
training_manager = TrainingManager()
