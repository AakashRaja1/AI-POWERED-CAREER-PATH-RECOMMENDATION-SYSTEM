from functools import lru_cache

from groq import Groq

from app.core.config import settings


@lru_cache(maxsize=1)
def get_groq_client() -> Groq:
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured in backend/.env")

    return Groq(api_key=settings.GROQ_API_KEY)