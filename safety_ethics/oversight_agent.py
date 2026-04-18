class OversightAgent:
    def __init__(self, risk_classifier):
        self.risk_classifier = risk_classifier

    def review(self, action):
        risk = self.risk_classifier.classify(action)
        if risk in ["high", "critical"]:
            return {"approved": False, "risk": risk}
        return {"approved": True, "risk": risk}
