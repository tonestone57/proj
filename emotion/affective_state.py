class AffectiveState:
    def __init__(self, decay_rate=0.05):
        self.valence = 0.0
        self.arousal = 0.0
        self.decay_rate = decay_rate

    def update(self, appraisal):
        # SGI 2026: Affective state dynamics with momentum
        if isinstance(appraisal, (int, float)):
            target_v = appraisal
            target_a = abs(appraisal)
        else:
            target_v = appraisal.get("valence", 0.0)
            target_a = appraisal.get("arousal", 0.0)

        # Update with momentum (70% current, 30% new)
        self.valence = max(-1.0, min(1.0, (self.valence * 0.7) + (target_v * 0.3)))
        self.arousal = max(0.0, min(1.0, (self.arousal * 0.7) + (target_a * 0.3)))

    def decay(self):
        # Emotions naturally return to zero over time
        self.valence *= (1 - self.decay_rate)
        self.arousal *= (1 - self.decay_rate)

    def snapshot(self):
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            "intensity": (self.valence**2 + self.arousal**2)**0.5
        }
