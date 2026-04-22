import math

class EmotionGenerator:
    def __init__(self):
        self.emotions = {"joy": 0.1, "fear": 0.1, "anger": 0.1, "curiosity": 0.1}

    def generate(self, stimuli):
        # SGI 2026: Map system signals to affective states
        entropy = stimuli.get("entropy", 0.5)
        success_rate = stimuli.get("success_rate", 1.0)

        # High entropy/uncertainty leads to increased curiosity but also fear
        self.emotions["curiosity"] += entropy * 0.2
        self.emotions["fear"] += (entropy ** 2) * 0.1

        # Success impacts joy and anger
        if success_rate > 0.8:
            self.emotions["joy"] += 0.15
            self.emotions["anger"] -= 0.1
        elif success_rate < 0.3:
            self.emotions["anger"] += 0.2
            self.emotions["joy"] -= 0.1

        # Damping to prevent runaway emotions
        for k in self.emotions:
            self.emotions[k] = max(0.0, min(1.0, self.emotions[k]))

        return self.emotions.copy()
