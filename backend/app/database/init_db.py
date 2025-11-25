from sqlmodel import SQLModel
from sqlalchemy import text
from app.database.session import engine
import logging

# Import models so they are registered on SQLModel.metadata
import app.database.models  # noqa: F401

logger = logging.getLogger(__name__)


def init_db():
    """Create database tables for all SQLModel models.

    Note: importing `app.database.models` ensures model classes are defined
    and registered on SQLModel.metadata before create_all() runs.
    """
    try:
        SQLModel.metadata.create_all(engine)
        
        # Ensure is_admin column exists (for existing databases)
        try:
            from sqlalchemy import text
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='user' AND column_name='is_admin'
                """))
                if not result.fetchone():
                    try:
                        conn.execute(text("ALTER TABLE \"user\" ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"))
                        conn.commit()
                        logger.info("Added is_admin column to User table")
                    except Exception as alter_error:
                        # Column might already exist or table doesn't exist yet
                        logger.debug(f"Could not add is_admin column: {alter_error}")
        except Exception as col_error:
            # Table might not exist yet, which is fine
            logger.debug(f"Could not check is_admin column: {col_error}")
        
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.warning(f"Could not create database tables: {e}")
        # Don't raise - allow server to start