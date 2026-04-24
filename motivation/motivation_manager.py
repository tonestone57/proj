import ray
from core.base import CognitiveModule
from core.drives import calculate_entropy
from motivation.reward_engine import IntrinsicRewardEngine
from motivation.curiosity import CuriosityModule
from motivation.uncertainty import UncertaintyModule
from motivation.novelty import NoveltyModule

@ray.remote
class MotivationManager(CognitiveModule):
    def __init__(self, world_model=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.reward_engine = IntrinsicRewardEngine()
        self.curiosity = CuriosityModule(world_model)
        self.uncertainty = UncertaintyModule()
        self.novelty = NoveltyModule()
        self.world_model = world_model

    def evaluate(self, action, predicted_state, actual_state):
        signals = {}
        signals["curiosity"] = self.curiosity.compute_curiosity(action, predicted_state, actual_state)
        signals["uncertainty_reduction"] = self.uncertainty.compute_uncertainty(actual_state)
        signals["novelty"] = self.novelty.compute_novelty(actual_state)
        signals["goal_progress"] = 0.5
        return self.reward_engine.compute(signals)

    def receive(self, message):
        if super().receive(message): return
        # Standard SGI 2026 message handling for MotivationManager

        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "motivation_evaluation":
            result = self.evaluate(message['data']['action'], message['data']['predicted_state'], message['data']['actual_state'])
            self.send_result("motivation_result", result)

            # SGI 2026: Entropy-driven curiosity
            state = message['data'].get('actual_state', {})
            entropy = calculate_entropy(state)

            if entropy > 0.8:
                print(f"[MotivationManager] High system entropy ({entropy:.4f}). Triggering curiosity research.")
                self.send_result("curiosity_research", {
                    "reason": "high_entropy",
                    "entropy": entropy,
                    "focus": "novelty_seeking"
                })