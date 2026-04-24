import time
import ray
from core.base import CognitiveModule

@ray.remote
class VersionManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.versions = {}

    def record_version(self, agent_id, version):
        self.versions[agent_id] = {
            "version": version,
            "timestamp": time.time()
        }

    def get_version(self, agent_id):
        return self.versions.get(agent_id)

    def receive(self, message):
        if super().receive(message): return

        """Standard SGI message receiver."""
        if message["type"] == "version_check":
            v = self.get_version(message["data"]["agent_id"])
            # In a real system, send_result would be used
            print(f"[VersionManager] Version for {message['data']['agent_id']}: {v}")