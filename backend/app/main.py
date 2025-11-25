from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.routers.items import router as items_router
from app.api.routers.auth import router as auth_router
from app.api.routers.admin import router as admin_router
from app.database.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    try:
        init_db()
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        # Don't raise - allow server to start even if DB init fails
        # This allows the server to start and show connection errors in API calls

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust as needed for your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)
app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"status": "ok", "service": "Career Recommendation API"}
