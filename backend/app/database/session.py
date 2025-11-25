from sqlmodel import create_engine, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create engine with sensible defaults for pooling and pre-ping to avoid stale
# connections. Use future-style engine behavior via SQLAlchemy 2.x compatibility.
# Don't fail at import time - let it fail when actually used
try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
    # Only log if logging is configured
    try:
        db_name = settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL
        logger.info(f"Database engine created for: {db_name}")
    except:
        pass
except Exception as e:
    # Log but don't raise - let it fail when actually connecting
    logger.warning(f"Warning creating database engine: {e}")
    # Still create engine with basic settings
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )


def get_session():
    """Get a database session"""
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Error getting database session: {e}")
        raise