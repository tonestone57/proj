
import ray
from core.base import CognitiveModule

@ray.remote
class StateManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.shared_state = {}

    def update(self, key, value):
        self.shared_state[key] = value

    def get(self, key):
        return self.shared_state.get(key)

    def receive(self, message):
        """Standard SGI message receiver."""
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "update_state":
            self.update(message["data"]["key"], message["data"]["value"])
        elif message["type"] == "get_state":
            result = self.get(message["data"]["key"])
            self.send_result("state_result", {"key": message["data"]["key"], "value": result})
