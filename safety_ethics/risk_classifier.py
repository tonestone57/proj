class RiskClassifier:
    def __init__(self):
        self.levels = ["low", "medium", "high", "critical"]

    def classify(self, action):
        score = 0
        if action.get("harm", False): score += 2
        if action.get("deception", False): score += 2
        if action.get("systemic_risk", False): score += 3
        if action.get("malicious_use", False): score += 3

        if score >= 5: return "critical"
        if score >= 3: return "high"
        if score >= 1: return "medium"
        return "low"
