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
        
        # Ensure is_admin and last_login columns exist (for existing databases)
        try:
            from sqlalchemy import text
            with engine.connect() as conn:
                required_columns = {
                    "is_admin": "ALTER TABLE \"user\" ADD COLUMN is_admin BOOLEAN DEFAULT FALSE",
                    "last_login": "ALTER TABLE \"user\" ADD COLUMN last_login TIMESTAMP NULL",
                }
                for column_name, alter_sql in required_columns.items():
                    result = conn.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name='user' AND column_name=:column_name
                    """), {"column_name": column_name})
                    if not result.fetchone():
                        try:
                            conn.execute(text(alter_sql))
                            conn.commit()
                            logger.info(f"Added {column_name} column to User table")
                        except Exception as alter_error:
                            # Column might already exist or table doesn't exist yet
                            logger.debug(f"Could not add {column_name} column: {alter_error}")
        except Exception as col_error:
            # Table might not exist yet, which is fine
            logger.debug(f"Could not check is_admin column: {col_error}")
        
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.warning(f"Could not create database tables: {e}")
        # Don't raise - allow server to start
        return False