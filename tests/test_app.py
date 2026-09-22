import pytest

from app import create_app, CloseAllState


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


def test_poll_reflects_pending_after_trigger(client):
    client.post("/api/trigger", headers={"X-Auth-Token": "phone-secret"})
    resp = client.get("/api/poll?token=ea-secret")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["pending"] is True
    assert body["issued_at"] is not None


def test_poll_before_any_trigger_is_not_pending(client):
    resp = client.get("/api/poll?token=ea-secret")
    assert resp.status_code == 200
    assert resp.get_json() == {"pending": False, "issued_at": None}


def test_poll_with_wrong_token_returns_404(client):
    resp = client.get("/api/poll?token=wrong")
    assert resp.status_code == 404


def test_ack_clears_pending(client):
    client.post("/api/trigger", headers={"X-Auth-Token": "phone-secret"})
    ack_resp = client.post("/api/ack", headers={"X-Auth-Token": "ea-secret"})
    assert ack_resp.status_code == 200
    assert ack_resp.get_json() == {"ok": True}

    poll_resp = client.get("/api/poll?token=ea-secret")
    assert poll_resp.get_json()["pending"] is False


def test_ack_with_wrong_token_returns_404(client):
    resp = client.post("/api/ack", headers={"X-Auth-Token": "wrong"})
    assert resp.status_code == 404


def test_pending_expires_after_five_minutes():
    clock = {"t": 0.0}
    state = CloseAllState(expiry_seconds=300, clock=lambda: clock["t"])
    app = create_app(phone_token="phone-secret", ea_token="ea-secret", state=state)
    app.testing = True
    test_client = app.test_client()

    test_client.post("/api/trigger", headers={"X-Auth-Token": "phone-secret"})
    clock["t"] = 301.0
    resp = test_client.get("/api/poll?token=ea-secret")
    assert resp.get_json()["pending"] is False
