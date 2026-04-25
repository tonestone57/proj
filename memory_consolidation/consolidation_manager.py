import ray
import asyncio
from core.base import CognitiveModule
from memory_consolidation.hippocampal_replay import HippocampalReplay
from memory_consolidation.generative_trainer import GenerativeTrainer
from memory_consolidation.consolidation_scheduler import ConsolidationScheduler
from memory_consolidation.schema_manager import SchemaManager

@ray.remote
class ConsolidationManager(CognitiveModule):
    def __init__(self, episodic_memory=None, generative_model=None, world_model=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.replay = HippocampalReplay.remote(episodic_memory, workspace, scheduler, model_registry)
        self.trainer = GenerativeTrainer.remote(generative_model, workspace, scheduler, model_registry)
        self.consolidation_scheduler = ConsolidationScheduler.remote(50, workspace, scheduler, model_registry)
        self.schemas = SchemaManager.remote(workspace, scheduler, model_registry)
        self.world_model = world_model
        self.episodic_memory = episodic_memory

    async def consolidate(self):
        # Handle remote episodic memory
        if not self.episodic_memory: return {"error": "No episodic memory"}

        try:
            # Assuming episodic_memory actor has 'get_episodes' method
            episodes = await self.episodic_memory.get_episodes.remote()
        except Exception:
            # Fallback for testing or non-actor objects
            episodes = getattr(self.episodic_memory, 'episodes', [])

        # Filter episodes using local scheduler
        selected = []
        for ep in episodes:
            if ep.get("strength", 0.5) < 0.5: # Hardcoded threshold for stability
                selected.append(ep)

        replay_batch = [ep["sensory"] for ep in selected]
        # trainer and schemas are remote actors
        loss = await self.trainer.train_on_replay.remote(replay_batch)

        # Concurrent schema updates
        await asyncio.gather(*[self.schemas.update_schema.remote(ep) for ep in selected])

        # Concurrent memory enrichment and world model synchronization
        async def enrich_and_sync(ep):
            enriched = await self.schemas.apply_schema.remote(ep)
            if self.world_model:
                try:
                    await self.world_model.update_entity.remote(ep["id"], enriched)
                except Exception:
                    pass
            return enriched

        await asyncio.gather(*[enrich_and_sync(ep) for ep in selected])

        return {"consolidation_loss": loss, "episodes": len(selected)}

    async def receive(self, message):
        if super().receive(message): return
        # Standard SGI 2026 message handling for ConsolidationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "consolidation_trigger":
            result = await self.consolidate()
            self.send_result("consolidation_result", result)
