import ray
import time
import asyncio
import os

# Core components
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from core.drives import DriveEngine
from core.config import CPU_CORES_MAX, MAX_THREADS, TICK_INTERVAL, SYSTEM_NAME, THERMAL_THRESHOLD_C

# Actors
from actors.reasoner_actor import ReasonerActor
from actors.coding_actor import CodingActor
from actors.search_actor import SearchActor
from actors.critic_actor import InternalCritic
from actors.planner import Planner
from memory.memory_manager import MemoryManager
from monitoring.thermal_guard import ThermalGuard

# Enforce thread limits for Intel i5-8265U (15W TDP)
os.environ["OMP_NUM_THREADS"] = str(MAX_THREADS)
os.environ["MKL_NUM_THREADS"] = str(MAX_THREADS)
os.environ["OPENBLAS_NUM_THREADS"] = str(MAX_THREADS)
os.environ["VECLIB_MAXIMUM_THREADS"] = str(MAX_THREADS)
os.environ["NUMEXPR_NUM_THREADS"] = str(MAX_THREADS)

# Ray Initialization
ray.init(ignore_reinit_error=True, num_cpus=CPU_CORES_MAX)

class SGIHub:
    def __init__(self, workspace, scheduler, thermal_guard):
        self.workspace = workspace
        self.scheduler = scheduler
        self.thermal_guard = thermal_guard
        self.state = {"focus": "idle", "history": []}

    async def safe_delegate(self, actor_handle, task_type, payload):
        """Check thermal health before every task."""
        if await self.thermal_guard.check_health.remote():
            print(f"[Hub] System is cool. Delegating {task_type}...")
            actor_handle.receive.remote({"type": task_type, "data": payload})
            return True
        else:
            print("🚨 Thermal Guard Active: CPU cooling down...")
            return False

    async def poll_scheduler(self):
        """Poll the scheduler and broadcast results to the workspace."""
        res_obj = await self.scheduler.next.remote()
        if res_obj:
            priority, actor_handle, message = res_obj
            print(f"[Hub] Processing result from scheduler: {message['type']}")
            self.workspace.broadcast.remote(message)

async def cognitive_cycle():
    # Initialize Core Actors
    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()
    thermal_guard = ThermalGuard.remote(threshold_temp=THERMAL_THRESHOLD_C)

    # Initialize Specialized Actors
    model_id = "intel/neural-chat-14b-v3-3"
    reasoner = ReasonerActor.remote(workspace, scheduler, model_id=model_id)
    coder = CodingActor.remote(workspace, scheduler, model_id=model_id)
    searcher = SearchActor.remote(workspace, scheduler, model_id=model_id)
    critic = InternalCritic.remote(workspace, scheduler, model_id=model_id)
    planner = Planner.remote(workspace, scheduler, model_id=model_id)
    memory_manager = MemoryManager.remote(workspace, scheduler)

    hub = SGIHub(workspace, scheduler, thermal_guard)
    drives = DriveEngine()

    print(f"--- {SYSTEM_NAME} Initialized for Intel i5-8265U ---")
    print("Architecture: Asynchronous Predictive Workspace (APW)")

    # The Heartbeat Loop
    for tick in range(10):
        print(f"\n--- Heartbeat Tick {tick+1} ---")

        # 1. Thermal & Resource Check
        health = await thermal_guard.get_thermal_state.remote()
        print(f"[Hub] Thermal State: Load={health['load']}%, Temp={health['temp']}C, Throttled={health['is_throttled']}")

        # 2. Drive: Proactive task triggering based on Entropy
        state = await workspace.get_current_state.remote()
        # Fixed nitpick: Use initialized DriveEngine instance
        entropy = drives.evaluate_state(state)
        print(f"[Hub] System Entropy: {entropy:.4f}")

        if entropy > 0.7: # Threshold from config.yaml
            print("[Drives] High Entropy detected. Triggering proactive tasks.")
            if tick % 2 == 0:
                await hub.safe_delegate(reasoner, "query", "math.factorial(6)")
            else:
                await hub.safe_delegate(coder, "code_execution", "print('Proactive self-test')")

        # 3. Poll Scheduler for asynchronous results
        await hub.poll_scheduler()

        await asyncio.sleep(TICK_INTERVAL)

    print(f"\n{SYSTEM_NAME} Demo complete.")

if __name__ == "__main__":
    asyncio.run(cognitive_cycle())
