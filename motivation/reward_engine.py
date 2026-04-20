import ray
from core.base import CognitiveModule
@ray.remote
class IntrinsicRewardEngine(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.weights = {
            "curiosity": 1.0,
            "uncertainty_reduction": 1.0,
            "novelty": 0.8,
            "goal_progress": 1.2
        }

    def compute(self, signals):
        reward = 0.0
        for key, value in signals.items():
            reward += self.weights.get(key, 0) * value
        return reward

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
