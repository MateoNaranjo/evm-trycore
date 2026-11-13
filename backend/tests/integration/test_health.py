from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok_status():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_spec_is_exposed_at_api_docs():
    response = client.get("/api-docs")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "EVM Tracker API"
