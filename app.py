import time
import hmac

from flask import Flask, request, abort, render_template, jsonify


class CloseAllState:
    def __init__(self, expiry_seconds=300, clock=time.time):
        self.pending = False
        self.issued_at = None
        self.expiry_seconds = expiry_seconds
        self._clock = clock

    def trigger(self):
        self.pending = True
        self.issued_at = self._clock()

    def is_active(self):
        if not self.pending or self.issued_at is None:
            return False
        if self._clock() - self.issued_at > self.expiry_seconds:
            self.pending = False
            return False
        return True

    def ack(self):
        self.pending = False
        self.issued_at = None


def _token_matches(provided, expected):
    if not expected:
        return False
    return hmac.compare_digest(provided or "", expected)


def create_app(phone_token, ea_token, state=None):
    app = Flask(__name__)
    app.state = state if state is not None else CloseAllState()

    @app.route("/close-all")
    def close_all_page():
        token = request.args.get("token", "")
        if not _token_matches(token, phone_token):
            abort(404)
        return render_template("confirm.html", token=token)

    @app.route("/api/trigger", methods=["POST"])
    def api_trigger():
        token = request.headers.get("X-Auth-Token", "")
        if not _token_matches(token, phone_token):
            abort(404)
        app.state.trigger()
        return jsonify(ok=True)

    @app.route("/api/poll")
    def api_poll():
        token = request.args.get("token", "")
        if not _token_matches(token, ea_token):
            abort(404)
        return jsonify(pending=app.state.is_active(), issued_at=app.state.issued_at)

    @app.route("/api/ack", methods=["POST"])
    def api_ack():
        token = request.headers.get("X-Auth-Token", "")
        if not _token_matches(token, ea_token):
            abort(404)
        app.state.ack()
        return jsonify(ok=True)

    return app


if __name__ == "__main__":
    import os

    flask_app = create_app(
        phone_token=os.environ.get("PHONE_TOKEN", "local-phone-token"),
        ea_token=os.environ.get("EA_TOKEN", "local-ea-token"),
    )
    flask_app.run(host="127.0.0.1", port=5000)
