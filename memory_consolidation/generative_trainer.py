import ray
from core.base import CognitiveModule

@ray.remote # SGI 2026: Standardized Ray Actor
class GenerativeTrainer(CognitiveModule):
    def __init__(self, generative_model, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.model = generative_model

    def train_on_replay(self, replay_batch):
        losses = []
        for sensory_input in replay_batch:
            loss = self.model.train_step(sensory_input)
            losses.append(loss)
        return sum(losses) / len(losses)
