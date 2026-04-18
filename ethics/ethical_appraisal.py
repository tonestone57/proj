class EthicalAppraisal:
    def __init__(self, norm_library):
        self.norms = norm_library.get_norms()

    def appraise(self, action):
        score = 0.0
        violations = []

        for norm, data in self.norms.items():
            if self.violates_norm(action, norm):
                score -= data["weight"]
                violations.append(norm)

        return score, violations

    def violates_norm(self, action, norm):
        # Placeholder logic
        if norm == "do_no_harm" and action.get("harm", False):
            return True
        if norm == "honesty" and action.get("deception", False):
            return True
        return False
