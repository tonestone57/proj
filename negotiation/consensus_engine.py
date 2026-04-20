import ray
from core.base import CognitiveModule
@ray.remote
class ConsensusEngine(CognitiveModule):
    def __init__(self, role_weights):
        self.role_weights = role_weights  # e.g. {"worker":1, "coordinator":2}

    def vote(self, agents, proposal):
        total = 0
        for agent in agents:
            weight = self.role_weights.get(agent.role, 1)
            total += weight * proposal.utility.get(agent.id, 0)
        return total

    def consensus(self, agents, proposals):
        return max(proposals, key=lambda p: self.vote(agents, p))

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
