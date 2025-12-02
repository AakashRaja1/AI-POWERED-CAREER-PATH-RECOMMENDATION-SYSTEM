from pathlib import Path
from pydantic_settings import BaseSettings

# BASE_DIR should point to the repository 'backend' directory (two levels up from this file)
# __file__ -> backend/app/core/config.py
# parents[2] -> backend
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "LatestCareerdataset.csv"

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/career_recommendations"
    MODEL_PATH: str = str(BASE_DIR / "model_artifacts")
    SECRET_KEY: str = "okchanged" # Default value, will be overridden by .env
    GROQ_API_KEY: str = ""  # Add this line for Groq API integration
    ADMIN_EMAIL: str = "admin@careerpath.com"  # Default admin email
    ADMIN_PASSWORD: str = "admin123"  # Default admin password - CHANGE IN PRODUCTION
    
    model_config = {
        "env_file": str(BASE_DIR / ".env"),
        "env_file_encoding": "utf-8"
    }

settings = Settings()
