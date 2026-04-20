import ray
from core.base import CognitiveModule
@ray.remote
class UtilityEngine(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)

    def compute(self, allocation, demand):
        return max(0, 1 - abs(allocation - demand))

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
