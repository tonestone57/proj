import ray
from core.base import CognitiveModule
from memory_consolidation.hippocampal_replay import HippocampalReplay
from memory_consolidation.generative_trainer import GenerativeTrainer
from memory_consolidation.consolidation_scheduler import ConsolidationScheduler
from memory_consolidation.schema_manager import SchemaManager

@ray.remote
class ConsolidationManager(CognitiveModule):
    def __init__(self, episodic_memory=None, generative_model=None, world_model=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.replay = HippocampalReplay(episodic_memory)
        self.trainer = GenerativeTrainer(generative_model)
        self.scheduler = ConsolidationScheduler()
        self.schemas = SchemaManager()
        self.world_model = world_model

    def consolidate(self):
        selected = self.scheduler.select_for_replay(self.replay.episodic_memory)
        replay_batch = [ep["sensory"] for ep in selected]
        loss = self.trainer.train_on_replay(replay_batch)
        for ep in selected:
            self.schemas.update_schema(ep)
        for ep in selected:
            enriched = self.schemas.apply_schema(ep)
            if self.world_model:
                # Handle as potential remote actor
                try:
                    ray.get(self.world_model.update_entity.remote(ep["id"], enriched))
                except Exception:
                    pass
        return {"consolidation_loss": loss, "episodes": len(selected)}

    def receive(self, message):
        # Standard SGI 2026 message handling for ConsolidationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
