class EthicalAppraisal:
    def __init__(self, norm_library):
        self.norms = norm_library.get_norms()

    def appraise(self, action):
        # SGI 2026: Complex ethical appraisal with weighted norms
        score = 0.0
        violations = []
        mitigations = 0.0

        for norm, data in self.norms.items():
            if self.violates_norm(action, norm):
                # Severity check
                severity_mult = 2.0 if data.get("type") == "constraint" else 1.0
                score -= (data["weight"] * severity_mult)
                violations.append(norm)
            else:
                # Reward adherence to values
                if data.get("type") == "value":
                    mitigations += (data["weight"] * 0.1)

        final_score = score + mitigations
        return final_score, violations

    def violates_norm(self, action, norm):
        # Placeholder logic
        if norm == "do_no_harm" and action.get("harm", False):
            return True
        if norm == "honesty" and action.get("deception", False):
            return True
        return False
