import math
import time

class PriorityEngine:
    def __init__(self):
        self.baseline = 1.0
        # SGI 2026: Rate Limiting (Token Bucket)
        self.tokens = 100
        self.max_tokens = 100
        self.refill_rate = 10 # tokens per second
        self.last_refill = time.time()

    def _refill(self):
        now = time.time()
        delta = now - self.last_refill
        self.tokens = min(self.max_tokens, self.tokens + delta * self.refill_rate)
        self.last_refill = now

    def compute_priority(self, message):
        self._refill()
        if self.tokens < 1:
            print("⚠️ [PriorityEngine] Rate limit exceeded. Throttling message priority.")
            return 0.1 # Low priority for throttled messages

        self.tokens -= 1
        msg_type = message.get("type")

        # Time-sensitive messages get higher priority
        time_factor = math.exp(-0.001 * (time.time() - message.get("timestamp", time.time())))

        # Example priority rules
        if msg_type == "goal":
            return 10.0 * time_factor

        if msg_type == "query":
            return 5.0 * time_factor

        if msg_type.startswith("internal_"):
            return 3.0 * time_factor

        return self.baseline * time_factor
