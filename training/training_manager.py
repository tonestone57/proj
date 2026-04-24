import ray
from core.base import CognitiveModule
from training.self_supervised import SelfSupervisedTrainer
from training.rl_trainer import RLTrainer
from training.curriculum import Curriculum
from training.world_model_trainer import WorldModelTrainer
from training.meta_learning import MetaLearning

@ray.remote
class TrainingManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None, modules=None, world_model=None, motivation=None):
        super().__init__(workspace, scheduler, model_registry)
        self.self_supervised = SelfSupervisedTrainer(modules)
        self.rl = RLTrainer(world_model, motivation)
        self.curriculum = Curriculum()
        self.world_model_trainer = WorldModelTrainer(world_model)
        self.meta = MetaLearning()

    def train(self, data, action, predicted_state, actual_state):
        ss_loss = self.self_supervised.train_step(data)
        reward = self.rl.train_step(action, predicted_state, actual_state)
        self.curriculum.update(reward)
        self.world_model_trainer.train_step(action, actual_state)
        self.meta.update(reward)
        return {
            "self_supervised_loss": ss_loss,
            "reward": reward,
            "curriculum_level": self.curriculum.level
        }

    def receive(self, message):
        if super().receive(message): return
        # Standard SGI 2026 message handling for TrainingManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "autonomous_training":
            print("[TrainingManager] Starting autonomous training step...")
            # Simulate background training data and states
            data = "Background system logs and experience traces"
            action = "Self-improvement"
            predicted_state = {"properties": {"efficiency": 0.8}}
            actual_state = {"properties": {"efficiency": 0.85}}
            result = self.train(data, action, predicted_state, actual_state)
            print(f"[TrainingManager] Autonomous training complete: Reward={result['reward']}")
