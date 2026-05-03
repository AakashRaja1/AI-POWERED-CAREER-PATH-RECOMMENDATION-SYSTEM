"""
Legacy route module kept for compatibility with earlier API paths. This file handles the   init   part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from app.routes.chatbot import router as chatbot_router
from app.routes.auth import router as auth_router

__all__ = ["chatbot_router", "auth_router"]
