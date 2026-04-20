import ray
from core.base import CognitiveModule
from motivation.reward_engine import IntrinsicRewardEngine
from motivation.curiosity import CuriosityModule
from motivation.uncertainty import UncertaintyModule
from motivation.novelty import NoveltyModule

@ray.remote
class MotivationManager(CognitiveModule):
    def __init__(self, world_model):
        self.reward_engine = IntrinsicRewardEngine()
        self.curiosity = CuriosityModule(world_model)
        self.uncertainty = UncertaintyModule()
        self.novelty = NoveltyModule()
        self.world_model = world_model

    def evaluate(self, action, predicted_state, actual_state):
        signals = {}

        # Curiosity
        signals["curiosity"] = self.curiosity.compute_curiosity(
            action, predicted_state, actual_state
        )

        # Uncertainty reduction
        signals["uncertainty_reduction"] = self.uncertainty.compute_uncertainty(
            actual_state
        )

        # Novelty
        signals["novelty"] = self.novelty.compute_novelty(actual_state)

        # Goal progress (placeholder)
        signals["goal_progress"] = 0.5

        return self.reward_engine.compute(signals)

from motivation.motivation_manager import MotivationManager

motivation = MotivationManager(world_model)
modules["motivation"] = motivation

if msg_type in ["evaluate_action"]:
    return module_registry.get("motivation")

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
