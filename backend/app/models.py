from pydantic import BaseModel, Field
from typing import Optional


class StudentInput(BaseModel):
    user_id: Optional[str] = Field(None, alias="User ID")
    full_name: str = Field(..., alias="Full Name")
    education_level: str = Field(..., alias="Education Level")
    academic_performance: str = Field(..., alias="Academic Performance")
    skills: str = Field(..., alias="Skills")
    certifications: Optional[str] = Field(None, alias="Certifications")
    work_preference: str = Field(..., alias="Do you prefer working with data, people, or ideas?")
    problem_solving: str = Field(..., alias="How do you approach solving complex problems?")
    environment_preference: str = Field(..., alias="Do you thrive better in a structured or flexible environment?")
    teamwork_preference: str = Field(..., alias="Do you prefer working independently or in a team?")
    learning_style: str = Field(..., alias="Do you learn best through practice, observation, or theory?")
    interests: str = Field(..., alias="Interests")
    extra_curricular: Optional[str] = Field(None, alias="Extra-Curricular Activities")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "str_strip_whitespace": True
    }


class PredictionOutput(BaseModel):
    best_fit_career_domain: str = Field(..., alias="Best-Fit Career Domain")
    confidence_score: float = Field(..., alias="Confidence Score")
    career_rationale: str = Field(..., alias="Career Rationale")
    growth_roadmap: str = Field(..., alias="5-Year Career Growth Roadmap")
    skill_gap_analysis: str = Field(..., alias="Skill Gap Analysis")
    recommended_courses: str = Field(..., alias="Recommended Tools, Courses, and Certifications")
    backup_career_option: str = Field(..., alias="Alternative/Backup Career Option")
    behavioral_insight: str = Field(..., alias="Behavioral Insight")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "str_strip_whitespace": True
    }
