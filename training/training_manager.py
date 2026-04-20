import ray
from core.base import CognitiveModule
from training.self_supervised import SelfSupervisedTrainer
from training.rl_trainer import RLTrainer
from training.curriculum import Curriculum
from training.world_model_trainer import WorldModelTrainer
from training.meta_learning import MetaLearning

@ray.remote
class TrainingManager(CognitiveModule):
    def __init__(self, modules, world_model, motivation):
        self.self_supervised = SelfSupervisedTrainer(modules)
        self.rl = RLTrainer(world_model, motivation)
        self.curriculum = Curriculum()
        self.world_model_trainer = WorldModelTrainer(world_model)
        self.meta = MetaLearning()

    def train(self, data, action, predicted_state, actual_state):
        # 1. Self-supervised learning
        ss_loss = self.self_supervised.train_step(data)

        # 2. RL update
        reward = self.rl.train_step(action, predicted_state, actual_state)

        # 3. Curriculum update
        self.curriculum.update(reward)

        # 4. World-model update
        self.world_model_trainer.train_step(action, actual_state)

        # 5. Meta-learning update
        self.meta.update(reward)

        return {
            "self_supervised_loss": ss_loss,
            "reward": reward,
            "curriculum_level": self.curriculum.level
        }

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
