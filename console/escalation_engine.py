
class EscalationEngine:
    def __init__(self, threshold=0.85):
        self.threshold = threshold

    def requires_human(self, confidence):
        return confidence < self.threshold
