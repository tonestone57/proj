Inspired by EICA’s emotion-generation mechanisms (bio-inspired, modular, grounded in affective computing) Springer.
class EmotionGenerator:
    def __init__(self):
        self.emotions = {"joy":0, "fear":0, "anger":0, "curiosity":0}

    def generate(self, stimuli):
        if stimuli.get("reward", 0) > 0:
            self.emotions["joy"] += 0.2
        if stimuli.get("threat", False):
            self.emotions["fear"] += 0.3
        if stimuli.get("obstacle", False):
            self.emotions["anger"] += 0.1
        if stimuli.get("novelty", False):
            self.emotions["curiosity"] += 0.25
        return self.emotions