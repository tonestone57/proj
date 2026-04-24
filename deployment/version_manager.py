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
        """Standard SGI message receiver."""
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "config_update":
            self.reload_config()
        elif message["type"] == "version_check":
            v = self.get_version(message["data"]["agent_id"])
            self.send_result("version_result", {"agent_id": message["data"]["agent_id"], "version": v})
