
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_research_rejects_short_topic():
    response = client.post(
        "/research",
        json={"topic": "AI"},
    )

    assert response.status_code == 422


def test_research_rejects_missing_topic():
    response = client.post(
        "/research",
        json={},
    )

    assert response.status_code == 422
