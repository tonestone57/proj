import ray
from core.base import CognitiveModule

@ray.remote
class DefenseOrchestrator(CognitiveModule):
    def orchestrate(self, agents, traffic):
        results = {}
        for agent in agents:
            results[agent.__class__.__name__] = agent(traffic)
        return results
