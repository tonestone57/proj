import ray
from core.config import WORKSPACE_HISTORY_LIMIT

@ray.remote
class GlobalWorkspace:
    def __init__(self):
        self.subscribers = []
        self.current_broadcast = None
        self.history = []

    def register(self, module):
        self.subscribers.append(module)

    def broadcast(self, message):
        self.current_broadcast = message
        self.history.append(message)
        # Keep history manageable using centralized config
        if len(self.history) > WORKSPACE_HISTORY_LIMIT:
            self.history.pop(0)

        for module in self.subscribers:
            # message is now a dict, we call receive.remote
            try:
                module.receive.remote(message)
            except Exception as e:
                print(f"[GlobalWorkspace] Error broadcasting to module: {e}")

    def get_current_state(self):
        return {
            "current_broadcast": self.current_broadcast,
            "history": self.history
        }
