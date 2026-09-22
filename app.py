import time


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
