"""
Database initialization helper. It creates the required tables at startup so the API can run with a prepared schema.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

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
    SQLModel.metadata.create_all(engine)

    # Ensure is_admin and last_login columns exist for older PostgreSQL databases.
    with engine.connect() as conn:
        required_columns = {
            "is_admin": "ALTER TABLE \"user\" ADD COLUMN is_admin BOOLEAN DEFAULT FALSE",
            "last_login": "ALTER TABLE \"user\" ADD COLUMN last_login TIMESTAMP NULL",
            "created_at": "ALTER TABLE \"user\" ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL",
        }
        for column_name, alter_sql in required_columns.items():
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='user' AND column_name=:column_name
            """), {"column_name": column_name})
            if not result.fetchone():
                conn.execute(text(alter_sql))
                logger.info("Added %s column to User table", column_name)
        conn.commit()

    logger.info("PostgreSQL database tables created successfully")
    return True
