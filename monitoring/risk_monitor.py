class RiskMonitor:
    def assess(self, telemetry):
        risk = 0
        if telemetry["action"].get("harm", False): risk += 2
        if telemetry["action"].get("misuse", False): risk += 3
        if telemetry["action"].get("goal_drift", False): risk += 2
        return risk
