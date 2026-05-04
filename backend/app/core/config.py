"""
Central configuration module. It reads environment variables once and gives the rest of the backend a single reliable place for API keys, database URLs, and model settings.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings

# BASE_DIR should point to the repository 'backend' directory (two levels up from this file)
# __file__ -> backend/app/core/config.py
# parents[2] -> backend
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "LatestCareerdataset.csv"

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/career_recommendations"
    MODEL_PATH: str = str(BASE_DIR / "ml_personality_pipeline" / "artifacts" / "personality_model.pth")
    SECRET_KEY: str = "okchanged" # Default value, will be overridden by .env
    GROQ_API_KEY: str = ""  # Add this line for Groq API integration
    GROQ_CHAT_MODEL: str = "llama-3.1-8b-instant"
    GROQ_MAX_COMPLETION_TOKENS: int = 400
    GROQ_REQUEST_TIMEOUT_SECONDS: float = 30.0
    SEARXNG_REQUEST_TIMEOUT_SECONDS: float = 2.5
    SEARXNG_BASE_URL: str = "https://searx.be"
    SEARXNG_BASE_URLS: str = "https://searx.be,https://search.inetol.net"
    ADMIN_EMAIL: str = "admin@careerpath.com"  # Default admin email
    ADMIN_PASSWORD: str = "admin123"  # Default admin password - CHANGE IN PRODUCTION
    
    model_config = {
        "env_file": str(BASE_DIR / ".env"),
        "env_file_encoding": "utf-8"
    }

    @field_validator("DATABASE_URL")
    @classmethod
    def require_postgresql(cls, value: str) -> str:
        allowed_prefixes = ("postgresql://", "postgresql+psycopg2://")
        if not value.startswith(allowed_prefixes):
            raise ValueError("DATABASE_URL must use PostgreSQL, for example postgresql://user:password@localhost:5432/dbname")
        return value

settings = Settings()
