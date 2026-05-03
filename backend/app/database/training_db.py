"""
Database module. It keeps persistence details separate from route handlers so the API code stays easier to explain and maintain. This file handles the training db part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from __future__ import annotations

import logging

from sqlmodel import SQLModel

from app.database.session import engine
from app.database.training_models import TrainingJob  # noqa: F401

logger = logging.getLogger(__name__)


def init_training_db() -> bool:
    """Create only the training job table.

    This intentionally avoids calling the shared project-wide init_db()
    so the rest of the application's tables and migrations remain untouched.
    """
    try:
        SQLModel.metadata.create_all(engine, tables=[TrainingJob.__table__])
        logger.info("Training job table created successfully")
        return True
    except Exception as exc:
        logger.warning(f"Could not create training job table: {exc}")
        return False