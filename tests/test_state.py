from app import CloseAllState


def test_starts_not_pending():
    state = CloseAllState()
    assert state.is_active() is False


def test_trigger_makes_it_active():
    state = CloseAllState()
    state.trigger()
    assert state.is_active() is True
    assert state.issued_at is not None


def test_ack_clears_pending():
    state = CloseAllState()
    state.trigger()
    state.ack()
    assert state.is_active() is False
    assert state.issued_at is None


def test_expires_after_configured_seconds():
    clock = {"t": 0.0}
    state = CloseAllState(expiry_seconds=300, clock=lambda: clock["t"])
    state.trigger()
    assert state.is_active() is True

    clock["t"] = 301.0
    assert state.is_active() is False


def test_still_active_just_before_expiry():
    clock = {"t": 0.0}
    state = CloseAllState(expiry_seconds=300, clock=lambda: clock["t"])
    state.trigger()

    clock["t"] = 299.0
    assert state.is_active() is True
