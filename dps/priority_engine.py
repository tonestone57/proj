import math
import time

class PriorityEngine:
    def __init__(self):
        self.baseline = 1.0

    def compute_priority(self, message):
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
