import ray
from core.base import CognitiveModule
@ray.remote
class ShutdownController(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.active = True

    def request_shutdown(self):
        self.active = False

    def is_active(self):
        return self.active

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
