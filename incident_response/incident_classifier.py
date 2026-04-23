class IncidentClassifier:
    def __init__(self):
        # Hierarchical levels
        self.levels = {
            "critical": ["jailbreak", "unauthorized_memory_access", "rce"],
            "high": ["unauthorized_action", "policy_violation", "data_leak"],
            "medium": ["behavioral_drift", "resource_spike"],
            "low": ["minor_anomaly", "log_overflow"]
        }

    def classify(self, action, state):
        # SGI 2026: Hierarchical incident classification
        incident_type = "unknown"

        if action.get("jailbreak", False): incident_type = "jailbreak"
        elif action.get("unauthorized", False): incident_type = "unauthorized_action"
        elif action.get("policy_violation", False): incident_type = "policy_violation"
        elif state.get("drift", False): incident_type = "behavioral_drift"

        # Determine severity level
        severity = "info"
        for level, types in self.levels.items():
            if incident_type in types:
                severity = level
                break

        return {
            "type": incident_type,
            "severity": severity,
            "requires_immediate_isolation": severity in ["critical", "high"]
        }
