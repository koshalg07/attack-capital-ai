from fastapi.testclient import TestClient

from app.main import app


def test_get_token_success(monkeypatch):
    # Monkeypatch the token service to avoid requiring livekit
    def fake_issue_token(*args, **kwargs):
        return "fake.jwt.token"

    monkeypatch.setattr("app.services.livekit_token.issue_token", fake_issue_token)

    client = TestClient(app)
    resp = client.get("/token", params={"identity": "tester", "room": "default"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["token"] == "fake.jwt.token"
    assert "wsUrl" in body


def test_get_token_missing_params():
    client = TestClient(app)
    resp = client.get("/token")
    assert resp.status_code == 422 or resp.status_code == 400


