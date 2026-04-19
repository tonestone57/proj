import time
import ray
from core.drives import DriveEngine
from core.config import THRESHOLD_REPLAN, THRESHOLD_CONSOLIDATE, TICK_INTERVAL

class CognitiveHeartbeat:
    def __init__(self, workspace, scheduler, planner=None, memory_manager=None):
        self.workspace = workspace
        self.scheduler = scheduler
        self.planner = planner
        self.memory_manager = memory_manager
        self.drive_engine = DriveEngine()
        self.last_tick = 0
        self.tick_interval = TICK_INTERVAL

    async def heartbeat_tick(self):
        state = await self.workspace.get_current_state.remote()
        entropy = self.drive_engine.evaluate_state(state)

        print(f"[Heartbeat] Current Entropy: {entropy:.4f}")

        if entropy > THRESHOLD_REPLAN:
            print("[Heartbeat] High System Entropy detected. Generating new strategy.")
            if self.planner:
                await self.scheduler.submit.remote(self.planner, {
                    "type": "goal",
                    "data": "Generate new strategy due to high system entropy",
                    "reason": "High System Entropy"
                })
        elif entropy < THRESHOLD_CONSOLIDATE:
            print("[Heartbeat] Low System Entropy detected. Triggering sleep cycle & Neural Archiving.")
            if self.memory_manager:
                await self.scheduler.submit.remote(self.memory_manager, {"type": "trigger_sleep_cycle"})
                # Archiving state data
                await self.memory_manager.perform_neural_archiving.remote(str(state))

        self.drive_engine.update_objective_priorities()
