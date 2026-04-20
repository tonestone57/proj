import ray
from core.base import CognitiveModule
@ray.remote
class ContextEngine(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)

    def adjust(self, demand, context):
        if context.get("peak_load", False):
            return demand * 0.8
        return demand

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
