from memory_consolidation.hippocampal_replay import HippocampalReplay
from memory_consolidation.generative_trainer import GenerativeTrainer
from memory_consolidation.consolidation_scheduler import ConsolidationScheduler
from memory_consolidation.schema_manager import SchemaManager

class ConsolidationManager:
    def __init__(self, episodic_memory, generative_model, world_model):
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
            self.world_model.state.update_entity(ep["id"], enriched)

        return {"consolidation_loss": loss, "episodes": len(selected)}

from memory_consolidation.consolidation_manager import ConsolidationManager

consolidation = ConsolidationManager(
    episodic_memory=modules["episodic_memory"],
    generative_model=modules["generative_model"],
    world_model=modules["world_model"]
)

modules["consolidation"] = consolidation

if msg_type in ["consolidate_memory"]:
    return module_registry.get("consolidation")
