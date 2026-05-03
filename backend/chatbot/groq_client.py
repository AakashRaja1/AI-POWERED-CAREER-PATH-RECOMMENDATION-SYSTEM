"""
Groq client factory. It validates the API key and creates the chat client used by both the chatbot and career recommendation features.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from functools import lru_cache

from groq import Groq

from app.core.config import settings


@lru_cache(maxsize=1)
def get_groq_client() -> Groq:
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured in backend/.env")

    return Groq(api_key=settings.GROQ_API_KEY)