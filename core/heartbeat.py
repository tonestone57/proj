import time
from core.drives import DriveEngine, THRESHOLD_REPLAN, THRESHOLD_CONSOLIDATE

class CognitiveHeartbeat:
    def __init__(self, workspace, scheduler, dps, planner=None, memory_manager=None):
        self.workspace = workspace
        self.scheduler = scheduler
        self.dps = dps
        self.planner = planner
        self.memory_manager = memory_manager
        self.drive_engine = DriveEngine()
        self.last_tick = 0
        self.tick_interval = 5.0 # Run entropy check every 5 seconds

    def heartbeat_tick(self):
        state = self.workspace.get_current_state()
        entropy = self.drive_engine.evaluate_state(state)

        print(f"[Heartbeat] Current Entropy: {entropy:.4f}")

        if entropy > THRESHOLD_REPLAN:
            print("[Heartbeat] High uncertainty detected. Triggering Re-planning.")
            if self.planner:
                # Submit to scheduler instead of direct call to maintain actor pattern
                self.scheduler.submit(self.planner, {"type": "goal", "data": "Address high system entropy"})
        elif entropy < THRESHOLD_CONSOLIDATE:
            print("[Heartbeat] Low uncertainty detected. Triggering Memory Consolidation.")
            if self.memory_manager:
                # Sleep cycle is a background process, but we can still submit a notification
                self.memory_manager.trigger_sleep_cycle()

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
