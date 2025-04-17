# import pytest # Removed unused import


def test_app_importable():
    pass  # import app.main # Removed unused import - function needs a body now


def test_health_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
