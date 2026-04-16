Based on AOM’s real-time control layer and enterprise oversight requirements.
microsoft.github.io California Management Review
class OversightAgent:
    def review(self, action):
        if action.get("high_risk", False):
            return False
        return True