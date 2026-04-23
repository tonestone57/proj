class OversightAgent:
    def __init__(self, id="oversight-01"):
        self.id = id

    def review(self, action):
        # SGI 2026: Real-time action review
        is_risky = action.get("type") in ["shutdown", "modify_core", "network_access"]

        if is_risky and action.get("priority", 0) < 0.9:
            return False

        return True
