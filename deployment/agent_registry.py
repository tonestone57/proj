import ray
from core.base import CognitiveModule
@ray.remote
class AgentRegistry(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.registry = {}

    def register(self, agent_id, metadata):
        self.registry[agent_id] = metadata

    def get(self, agent_id):
        return self.registry.get(agent_id)

    def all_agents(self):
        return self.registry

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
