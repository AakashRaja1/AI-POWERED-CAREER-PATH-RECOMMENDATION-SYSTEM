import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.main import app

# Create an in-memory SQLite engine for tests
TEST_SQLITE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine_and_tables():
    # Create engine and create all tables once per test session
    engine = create_engine(TEST_SQLITE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    # No explicit teardown needed for in-memory DB; it is discarded when process exits


@pytest.fixture()
def db_session(engine_and_tables):
    engine = engine_and_tables
    with Session(engine) as session:
        yield session


@pytest.fixture()
def client(monkeypatch, engine_and_tables):
    """FastAPI TestClient that overrides the app's get_session dependency to use
    the in-memory SQLite session. This isolates tests from the real Postgres DB.
    """
    from app.database.session import get_session as real_get_session

    def _get_test_session():
        # Each call yields a new Session against the in-memory engine
        with Session(engine_and_tables) as s:
            yield s

    # Monkeypatch the dependency used in routers (depends on import path)
    monkeypatch.setattr("app.database.session.get_session", lambda: _get_test_session())

    # Create a TestClient using the app with the overridden dependency
    with TestClient(app) as c:
        yield c
