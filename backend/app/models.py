from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union, List


class StudentInput(BaseModel):
    user_id: Optional[str] = Field(None, alias="User ID")
    full_name: str = Field(..., alias="Full Name")
    education_level: str = Field(..., alias="Education Level")
    academic_performance: Optional[str] = Field(None, alias="Academic Performance")
    skills: Union[str, List[str]] = Field(..., alias="Skills")
    certifications: Optional[str] = Field(None, alias="Certifications")
    work_preference: Optional[str] = Field(None, alias="Do you prefer working with data, people, or ideas?")
    problem_solving: Optional[str] = Field(None, alias="How do you approach solving complex problems?")
    environment_preference: Optional[str] = Field(None, alias="Do you thrive better in a structured or flexible environment?")
    teamwork_preference: Optional[str] = Field(None, alias="Do you prefer working independently or in a team?")
    learning_style: Optional[str] = Field(None, alias="Do you learn best through practice, observation, or theory?")
    interests: Union[str, List[str]] = Field(..., alias="Interests")
    extra_curricular: Optional[str] = Field(None, alias="Extra-Curricular Activities")

    # Normalize list-like inputs to a clean comma-separated string
    @field_validator("skills", "interests")
    @classmethod
    def normalize_list_like(cls, v):
        if isinstance(v, list):
            return ", ".join([str(item).strip() for item in v if str(item).strip()])
        return str(v).strip()

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "str_strip_whitespace": True,
    }


class PredictionOutput(BaseModel):
    # Make fields optional with safe defaults to avoid 422 if model omits any
    best_fit_career_domain: Optional[str] = Field("", alias="Best-Fit Career Domain")
    confidence_score: Optional[float] = Field(0.0, alias="Confidence Score")
    career_rationale: Optional[str] = Field("", alias="Career Rationale")
    growth_roadmap: Optional[str] = Field("", alias="5-Year Career Growth Roadmap")
    skill_gap_analysis: Optional[str] = Field("", alias="Skill Gap Analysis")
    recommended_courses: Optional[str] = Field("", alias="Recommended Tools, Courses, and Certifications")
    backup_career_option: Optional[str] = Field("", alias="Alternative/Backup Career Option")
    behavioral_insight: Optional[str] = Field("", alias="Behavioral Insight")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "str_strip_whitespace": True,
    }
