"""
Database table definitions for application users, saved predictions, and admin-related fields. These SQLModel classes describe how Python objects are stored in PostgreSQL.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(unique=True, index=True)
    password: str
    is_admin: bool = Field(default=False)
    last_login: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    best_fit_career_domain: str
    confidence_score: float
    career_rationale: str
    growth_roadmap: str
    skill_gap_analysis: str
    recommended_courses: str
    backup_career_option: str
    behavioral_insight: str
