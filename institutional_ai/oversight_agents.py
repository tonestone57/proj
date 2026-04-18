class OversightAgent:
    def review(self, action):
        if action.get("high_risk", False):
            return False
        return True
