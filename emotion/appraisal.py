Evaluates events and assigns emotional meaning.
class EmotionalAppraisal:
    def __init__(self):
        self.rules = {
            "threat": -1.0,
            "opportunity": 1.0,
            "social_rejection": -0.8,
            "social_support": 0.9,
            "uncertainty": -0.4,
            "novelty": 0.3
        }

    def appraise(self, event):
        event_type = event.get("type")
        return self.rules.get(event_type, 0.0)
This is the AGI’s fast, System-1 emotional evaluation.