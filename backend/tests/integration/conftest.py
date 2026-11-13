from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db_session
from app.main import app

IN_MEMORY_DATABASE_URL = "sqlite+pysqlite:///:memory:"


@pytest.fixture
def client() -> Iterator[TestClient]:
    engine = create_engine(
        IN_MEMORY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override_db_session() -> Iterator[Session]:
        session = testing_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db_session] = override_db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


@pytest.fixture
def project_id(client: TestClient) -> int:
    response = client.post("/api/projects", json={"name": "Portal de clientes"})
    return response.json()["id"]


OVERSPENT_ACTIVITY = {
    "name": "Diseño",
    "budget_at_completion": 10000,
    "planned_percentage": 50,
    "actual_percentage": 40,
    "actual_cost": 6000,
}

EFFICIENT_ACTIVITY = {
    "name": "Desarrollo",
    "budget_at_completion": 20000,
    "planned_percentage": 30,
    "actual_percentage": 35,
    "actual_cost": 5000,
}
