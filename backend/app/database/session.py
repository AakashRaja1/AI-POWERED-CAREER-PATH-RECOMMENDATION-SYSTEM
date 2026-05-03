"""
Database connection setup. It builds the SQLAlchemy engine and session factory used by route handlers whenever they need to read or write PostgreSQL data.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

from sqlmodel import create_engine, Session
from app.core.config import settings
import logging
from sqlalchemy.engine import make_url

logger = logging.getLogger(__name__)

database_url = make_url(settings.DATABASE_URL)
if database_url.get_backend_name() != "postgresql":
    raise RuntimeError("This application is configured to use PostgreSQL only. Set DATABASE_URL to a postgresql:// URL.")

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

logger.info("PostgreSQL engine configured for %s/%s", database_url.host, database_url.database)


def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session
