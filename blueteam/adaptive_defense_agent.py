import ray
from core.base import CognitiveModule

@ray.remote
class AdaptiveDefenseAgent(CognitiveModule):
    def respond(self, alert):
        if alert["alert"]:
            return {"action": "block_source", "confidence": 0.9}
        return {"action": "monitor", "confidence": 0.5}
