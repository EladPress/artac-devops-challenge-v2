import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_returns_ready(client):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["model_loaded"] is True


def test_predict_positive_text(client):
    response = client.post("/predict", json={"text": "This movie was absolutely wonderful and amazing!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] in ("positive", "negative")
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_negative_text(client):
    response = client.post("/predict", json={"text": "This was terrible, I hated every minute of it."})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] in ("positive", "negative")
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_empty_text_rejected(client):
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422


def test_predict_missing_text_rejected(client):
    response = client.post("/predict", json={})
    assert response.status_code == 422
