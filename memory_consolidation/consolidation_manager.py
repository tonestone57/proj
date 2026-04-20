from memory_consolidation.hippocampal_replay import HippocampalReplay
from memory_consolidation.generative_trainer import GenerativeTrainer
from memory_consolidation.consolidation_scheduler import ConsolidationScheduler
from memory_consolidation.schema_manager import SchemaManager

class ConsolidationManager:
    def __init__(self):
        self.replay = HippocampalReplay()
        self.trainer = GenerativeTrainer()
        self.scheduler = ConsolidationScheduler()
        self.schemas = SchemaManager()

    def consolidate(self, memories):
        replayed = self.replay.replay(memories)
        trained = self.trainer.train(replayed)
        self.schemas.update(trained)
        return trained
