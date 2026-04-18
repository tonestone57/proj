import time
from core.drives import DriveEngine
from core.config import THRESHOLD_REPLAN, THRESHOLD_CONSOLIDATE, TICK_INTERVAL

class CognitiveHeartbeat:
    def __init__(self, workspace, scheduler, dps, planner=None, memory_manager=None):
        self.workspace = workspace
        self.scheduler = scheduler
        self.dps = dps
        self.planner = planner
        self.memory_manager = memory_manager
        self.drive_engine = DriveEngine()
        self.last_tick = 0
        self.tick_interval = TICK_INTERVAL

    def heartbeat_tick(self):
        state = self.workspace.get_current_state()
        entropy = self.drive_engine.evaluate_state(state)

        print(f"[Heartbeat] Current Entropy: {entropy:.4f}")

        if entropy > THRESHOLD_REPLAN:
            # High uncertainty: The agent is "confused" or facing a new problem
            print("[Heartbeat] High System Entropy detected. Generating new strategy.")
            if self.planner:
                # Trigger planner to generate new strategy due to high uncertainty
                self.scheduler.submit(self.planner, {
                    "type": "goal",
                    "data": "Generate new strategy due to high system entropy",
                    "reason": "High System Entropy"
                })
        elif entropy < THRESHOLD_CONSOLIDATE:
            # Low uncertainty: The agent is "bored"
            print("[Heartbeat] Low System Entropy detected. Triggering sleep cycle.")
            if self.memory_manager:
                # Trigger background consolidation: refactoring, indexing, synthetic data gen
                self.scheduler.submit(self.memory_manager, {"type": "trigger_sleep_cycle"})

        self.drive_engine.update_objective_priorities()

    def run(self):
        while True:
            # 1. Process as many scheduled tasks as possible without blocking
            task_processed = False
            while True:
                task = self.scheduler.next()
                if task is None:
                    break

                priority, module, message = task
                self.dps.process(message)
                task_processed = True

            # 2. Run heartbeat tick on interval
            current_time = time.time()
            if current_time - self.last_tick >= self.tick_interval:
                self.heartbeat_tick()
                self.last_tick = current_time

            # 3. Brief sleep to prevent 100% CPU usage if idle
            if not task_processed:
                time.sleep(0.1)
            else:
                # If we processed tasks, yield briefly
                time.sleep(0.01)
