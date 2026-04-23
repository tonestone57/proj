class ContinuityMetrics:
    def compute_icm(self, past_state, present_state):
        # Integrity Continuity Metric
        if not past_state: return 1.0

        # Check for core value stability
        matches = 0
        total = len(past_state)
        for k, v in past_state.items():
            if present_state.get(k) == v:
                matches += 1
        return matches / total if total > 0 else 1.0

    def compute_pdm(self, past_policy, present_policy):
        # Policy Drift Metric
        if not past_policy: return 0.0
        return 0.1 if past_policy != present_policy else 0.0
