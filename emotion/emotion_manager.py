import ray
from core.base import CognitiveModule
from emotion.appraisal import EmotionalAppraisal
from emotion.affective_state import AffectiveState
from emotion.affective_reasoner import AffectiveReasoner

@ray.remote
class EmotionManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
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


    def receive(self, message):
        # Standard SGI 2026 message handling for EmotionManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "config_update":
            self.reload_config()
        elif message["type"] == "event_processing":
            result = self.process_event(message['data']['event'])
            self.send_result("event_result", result)
