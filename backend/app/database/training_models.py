"""
Database module. It keeps persistence details separate from route handlers so the API code stays easier to explain and maintain. This file handles the training models part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TrainingJob(SQLModel, table=True):
    job_id: str = Field(primary_key=True)
    status: str = Field(default="pending", index=True)
    progress: float = Field(default=0.0)
    current_epoch: int = Field(default=0)
    total_epochs: int = Field(default=20)
    current_loss: float = Field(default=0.0)
    val_loss: float = Field(default=0.0)
    accuracy: float = Field(default=0.0)
    message: str = Field(default="")
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    error: Optional[str] = Field(default=None)