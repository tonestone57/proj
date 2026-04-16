Implements MI9’s finite-state conformance checking. arXiv.org
class ConformanceEngine:
    def check(self, action, allowed_actions):
        return action in allowed_actions