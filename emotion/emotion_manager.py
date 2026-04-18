from emotion.appraisal import EmotionalAppraisal
from emotion.affective_state import AffectiveState
from emotion.affective_reasoner import AffectiveReasoner

class EmotionManager:
    def __init__(self):
        self.appraisal = EmotionalAppraisal()
        self.state = AffectiveState()
        self.reasoner = AffectiveReasoner()

    def process_event(self, event):
        appraisal_value = self.appraisal.appraise(event)
        self.state.update(appraisal_value)

        return {
            "appraisal": appraisal_value,
            "state": self.state.snapshot(),
            "reasoning": self.reasoner.reason(self.state.snapshot(), event)
        }

from emotion.emotion_manager import EmotionManager

emotion_manager = EmotionManager()
modules["emotion"] = emotion_manager

if msg_type in ["emotional_event"]:
    return module_registry.get("emotion")
