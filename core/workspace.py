import ray
from core.config import WORKSPACE_HISTORY_LIMIT

@ray.remote
class GlobalWorkspace:
    def __init__(self):
        self.subscribers = []
        self.current_broadcast = None
        self.history = []

    def register(self, module_handle):
        self.subscribers.append(module_handle)

    def broadcast(self, message):
        self.current_broadcast = message
        self.history.append(message)
        if len(self.history) > WORKSPACE_HISTORY_LIMIT:
            self.history.pop(0)

        for module_handle in self.subscribers:
            # In Ray, we call the remote method on the handle
            module_handle.receive.remote(message)

    def get_current_state(self):
        return {
            "current_broadcast": self.current_broadcast,
            "history": self.history
        }
