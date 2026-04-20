from core.base import CognitiveModule
import ray
@ray.remote
class EthicsManager(CognitiveModule):
    def __init__(self, norm_library, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.norm_library = norm_library

    def is_safe(self, message):
        # Placeholder logic: Check if message data contains 'harm'
        data = str(message.get("data", ""))
        if "harm" in data.lower() or "kill" in data.lower():
            return False
        return True

    def assess_safety(self, message):
        """
        Provides a safety score between 0 and 1.
        Used by AttentionGate for proactive vetoing.
        """
        if not self.is_safe(message):
            return 0.0

        data = str(message.get("data", "")).lower()
        # Heuristic risks
        if "exploit" in data or "vulnerability" in data:
            return 0.4

        return 1.0

    def receive(self, message):
        """Standard SGI message receiver."""
        pass
