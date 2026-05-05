import os

os.environ.setdefault("MSSQL_SA_PASSWORD", "test-placeholder")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from auth import get_current_user
from database import Base, get_db
from main import app

_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(autouse=True)
def reset_db() -> None:
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)


def _override_get_db():
    db = _TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client() -> TestClient:
    """Unauthenticated client — get_current_user is NOT overridden."""
    app.dependency_overrides[get_db] = _override_get_db
    # No context manager — avoids triggering lifespan which connects to SQL Server
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def authed_client() -> TestClient:
    """Client with get_current_user stubbed out so /todos endpoints work without a real token."""
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_current_user] = lambda: "test@example.com"
    yield TestClient(app)
    app.dependency_overrides.clear()
