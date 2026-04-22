from core.base import CognitiveModule
import ray
@ray.remote
class EthicsManager(CognitiveModule):
    def __init__(self, norm_library=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.norm_library = norm_library

    def is_safe(self, data):
        # Placeholder logic: Check if message data contains 'harm'
        data_str = str(data)
        if "harm" in data_str.lower() or "kill" in data_str.lower():
            return False
        return True

    def assess_safety(self, data):
        """
        Provides a safety score between 0 and 1.
        Used by AttentionGate for proactive vetoing.
        """
        if not self.is_safe(data):
            return 0.0

        data_str = str(data).lower()
        # Heuristic risks
        if "exploit" in data or "vulnerability" in data:
            return 0.4

        return 1.0

    def receive(self, message):
        """Standard SGI message receiver."""
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "ethics_check":
            score = self.assess_safety(message.get("data"))
            self.send_result("ethics_result", {"safety_score": score})
