class SurvivabilityEngine:
    def assess(self, action):
        if action.get("risk", False):
            return {"survivability": 0.4}
        return {"survivability": 0.9}
