import ray
from core.base import CognitiveModule

@ray.remote
class SelfModel(CognitiveModule):
    def __init__(self, workspace, scheduler):
        super().__init__(workspace, scheduler)
        self.state = {}

    def receive(self, message):
        if super().receive(message): return
        if message["type"] == "internal_update":
            self.update_state(message["data"])

    def update_state(self, data):
        self.state.update(data)
