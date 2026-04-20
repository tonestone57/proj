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
        # 1. Select episodes for replay
        selected = self.scheduler.select_for_replay(self.replay.episodic_memory)

        # 2. Train generative model on replay
        replay_batch = [ep["sensory"] for ep in selected]
        loss = self.trainer.train_on_replay(replay_batch)

        # 3. Update schemas
        for ep in selected:
            self.schemas.update_schema(ep)

        # 4. Update world-model with consolidated knowledge
        for ep in selected:
            enriched = self.schemas.apply_schema(ep)
            if self.world_model:
                self.world_model.state.update_entity(ep["id"], enriched)

        return {"consolidation_loss": loss, "episodes": len(selected)}

    def receive(self, message):
        # Standard SGI 2026 message handling for ConsolidationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
