from core.base import CognitiveModule
import ray
@ray.remote
class VersionManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.versions = {}

    def record_version(self, agent_id, version):
        self.versions.setdefault(agent_id, []).append(version)

    def latest(self, agent_id):
        return self.versions.get(agent_id, [])[-1]

    def receive(self, message):
        """Standard SGI message receiver."""
        pass
