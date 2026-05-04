"""
FastAPI application entry point. It starts the API, prepares database tables, enables frontend access through CORS, and connects every router used by the career recommendation system.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.routers.auth import router as auth_router
from app.api.routers.admin import router as admin_router
from app.api.routers.personality import router as personality_router
from app.database.init_db import init_db
from chatbot.routes import router as chatbot_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("PostgreSQL database tables initialized successfully")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    # Support Vite fallback ports (e.g., 5175, 5176, 5180) during local development.
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(personality_router)
app.include_router(chatbot_router, prefix="/chatbot")

# Backward-compatible API aliases used by tests/frontend clients.
app.include_router(auth_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(personality_router, prefix="/api")
app.include_router(chatbot_router, prefix="/api/chatbot")

@app.get("/")
def root():
    return {"status": "ok", "service": "Career Recommendation API"}
