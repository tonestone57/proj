Inspired by AWS/Boomi’s Agent Control Tower for managing agent sprawl, compliance, and lifecycle. AWS
class AgentRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, agent_id, metadata):
        self.registry[agent_id] = metadata

    def get(self, agent_id):
        return self.registry.get(agent_id)

    def all_agents(self):
        return self.registry