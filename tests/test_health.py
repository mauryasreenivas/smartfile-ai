from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "SmartFile AI"
    assert body["version"] == "0.1.0"
    assert body["docs"] == "/docs"


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["application"] == "SmartFile AI"
    assert body["version"] == "0.1.0"
    assert body["environment"] == "testing"
    assert body["timestamp_utc"]
