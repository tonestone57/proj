Grounded in international AI risk-management frameworks (2023–2025) that integrate traditional risk management with AI safety. airisk.mit.edu
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
This implements risk-tiering, consistent with global AI safety frameworks.