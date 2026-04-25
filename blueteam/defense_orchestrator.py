import ray
from core.base import CognitiveModule

@ray.remote # SGI 2026: Standardized Ray Actor
class DefenseOrchestrator(CognitiveModule):
    def orchestrate(self, agents, traffic):
        results = {}
        for agent in agents:
            results[agent.__class__.__name__] = agent(traffic)
        return results
