class EmotionRegulator:
    def regulate(self, emotions):
        regulated = {k: min(v, 1.0) for k, v in emotions.items()}
        return regulated
