import ray
from core.base import CognitiveModule

@ray.remote
class SelfModel(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.state = {}

    def receive(self, message):
        try: super().receive(message)
        except NotImplementedError: pass
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "internal_update":
            self.update_state(message["data"])

    def update_state(self, data):
        self.state.update(data)