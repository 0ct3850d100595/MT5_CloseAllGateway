import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app(phone_token="phone-secret", ea_token="ea-secret")
    app.testing = True
    return app.test_client()


def test_close_all_page_correct_token_returns_200(client):
    resp = client.get("/close-all?token=phone-secret")
    assert resp.status_code == 200
    assert b"phone-secret" in resp.data


def test_close_all_page_wrong_token_returns_404(client):
    resp = client.get("/close-all?token=wrong")
    assert resp.status_code == 404


def test_close_all_page_missing_token_returns_404(client):
    resp = client.get("/close-all")
    assert resp.status_code == 404


def test_trigger_with_correct_token_sets_pending(client):
    resp = client.post("/api/trigger", headers={"X-Auth-Token": "phone-secret"})
    assert resp.status_code == 200
    assert resp.get_json() == {"ok": True}


def test_trigger_with_wrong_token_returns_404(client):
    resp = client.post("/api/trigger", headers={"X-Auth-Token": "wrong"})
    assert resp.status_code == 404
