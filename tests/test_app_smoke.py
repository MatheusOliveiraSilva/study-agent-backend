import pytest

def test_app_importable():
    import app.main

def test_health_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
