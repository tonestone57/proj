class AffectiveState:
    def __init__(self):
        self.valence = 0.0
        self.arousal = 0.0

    def update(self, appraisal_value):
        # Simple affective dynamics
        self.valence = max(-1.0, min(1.0, self.valence + appraisal_value * 0.1))
        self.arousal = max(0.0, min(1.0, self.arousal + abs(appraisal_value) * 0.05))

    def snapshot(self):
        return {
            "valence": self.valence,
            "arousal": self.arousal
        }
