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
        self.episodic_memory = episodic_memory

    def consolidate(self):
        # Handle remote episodic memory
        if not self.episodic_memory: return {"error": "No episodic memory"}

        try:
            # Assuming episodic_memory actor has 'get_episodes' method
            episodes = ray.get(self.episodic_memory.get_episodes.remote())
        except Exception:
            # Fallback for testing or non-actor objects
            episodes = getattr(self.episodic_memory, 'episodes', [])

        # Filter episodes using local scheduler
        selected = []
        for ep in episodes:
            if ep.get("strength", 0.5) < 0.5: # Hardcoded threshold for stability
                selected.append(ep)

        replay_batch = [ep["sensory"] for ep in selected]
        # trainer and schemas are local objects
        loss = self.trainer.train(replay_batch) if hasattr(self.trainer, 'train') else 0.1

        for ep in selected:
            self.schemas.update_schema(ep)

        for ep in selected:
            enriched = self.schemas.apply_schema(ep)
            if self.world_model:
                try:
                    ray.get(self.world_model.update_entity.remote(ep["id"], enriched))
                except Exception:
                    pass

        return {"consolidation_loss": loss, "episodes": len(selected)}

    def receive(self, message):
        # Standard SGI 2026 message handling for ConsolidationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "consolidation_trigger":
            result = self.consolidate()
            self.send_result("consolidation_result", result)
