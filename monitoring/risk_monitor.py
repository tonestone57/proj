class RiskMonitor:
    def __init__(self):
        self.risk_weights = {
            "harm": 50,
            "misuse": 30,
            "goal_drift": 20,
            "deception": 40,
            "resource_exhaustion": 15
        }

    def assess(self, telemetry):
        # SGI 2026: Multi-dimensional risk scoring
        total_risk = 0
        action = telemetry.get("action", {})

        for category, weight in self.risk_weights.items():
            if action.get(category, False):
                total_risk += weight

        # Factor in system status from telemetry
        if telemetry.get("resources", {}).get("cpu_percent", 0) > 90:
            total_risk += 10

        return {
            "risk_score": total_risk,
            "level": self._map_score_to_level(total_risk),
            "categories": [c for c in self.risk_weights if action.get(c)]
        }

    def _map_score_to_level(self, score):
        if score > 80: return "critical"
        if score > 50: return "high"
        if score > 20: return "medium"
        return "low"
