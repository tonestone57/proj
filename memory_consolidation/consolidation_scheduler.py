import ray
from core.base import CognitiveModule

@ray.remote # SGI 2026: Standardized Ray Actor
class ConsolidationScheduler(CognitiveModule):
    def __init__(self, interval_ticks=50, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.priority_threshold = 0.5
        self.interval = interval_ticks
        self.last_run = 0

    def should_start_sleep_cycle(self, current_tick, system_entropy):
        # SGI 2026: Consolidation triggered by time or low system activity
        if current_tick - self.last_run >= self.interval:
            return True
        if system_entropy < 0.2: # System is idle/stable
            return True
        return False

    def select_for_replay(self, episodes):
        # SGI 2026: Importance-based replay selection
        # Higher significance or novelty episodes are prioritized
        selected = sorted(episodes,
                         key=lambda e: e.get("significance", 0.5) * e.get("novelty", 1.0),
                         reverse=True)

        self.last_run += 1 # Track run attempt
        return selected[:10] # Limit replay batch size
