import ray
import time
import asyncio
import psutil
import yaml
import os

# Enforce 4-thread limit for 2026 hardware standard
MAX_THREADS = "4"
os.environ["OMP_NUM_THREADS"] = MAX_THREADS
os.environ["MKL_NUM_THREADS"] = MAX_THREADS
os.environ["OPENBLAS_NUM_THREADS"] = MAX_THREADS
os.environ["VECLIB_MAXIMUM_THREADS"] = MAX_THREADS
os.environ["NUMEXPR_NUM_THREADS"] = MAX_THREADS

# Core components
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from core.drives import DriveEngine

# Actors
from actors.reasoner_actor import ReasonerActor
from actors.coding_actor import CodingActor
from actors.search_actor import SearchActor
from actors.critic_actor import InternalCritic
from memory.memory_manager import MemoryManager
from monitoring.thermal_guard import ThermalGuard

# Load Manifest
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Ray Initialization
ray.init(num_cpus=config['hardware_limits']['ray_reserved_threads'], ignore_reinit_error=True)

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
            # Use Ray remote call on the handle
            return await actor_handle.receive.remote({"type": task_type, "data": payload})
        else:
            print("🚨 Thermal Guard Active: CPU cooling down...")
            await asyncio.sleep(5)
            return "Task delayed due to thermal pressure."

    async def integrate(self, results):
        for res in results:
            print(f"[Hub] Integrating result: {res}")
            self.state["history"].append(res)
        return self.state

async def cognitive_cycle():
    # Initialize Core Actors
    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()
    thermal_guard = ThermalGuard.remote(threshold_temp=config['hardware_limits']['thermal_threshold_celsius'])

    # Initialize Specialized Actors
    # Using the preferred self-reliant Intel model
    model_id = "intel/neural-chat-14b-v3-3"
    reasoner = ReasonerActor.remote(workspace, scheduler, model_id=model_id)
    coder = CodingActor.remote(workspace, scheduler, model_id=model_id)
    searcher = SearchActor.remote(workspace, scheduler, model_id=model_id)
    critic = InternalCritic.remote(workspace, scheduler, model_id=model_id)
    memory_manager = MemoryManager.remote(workspace, scheduler)

    hub = SGIHub(workspace, scheduler, thermal_guard)
    drives = DriveEngine()

    print(f"--- {config['system_identity']['name']} Initialized for Intel i5-8265U ---")
    print(f"Mode: {config['system_identity']['mode']}")

    # The Heartbeat Loop
    for tick in range(5):
        print(f"\n--- Heartbeat Tick {tick+1} ---")

        # 1. Check health
        health = await thermal_guard.get_thermal_state.remote()
        print(f"[Hub] Thermal State: Load={health['load']}%, Temp Throttled={health['is_throttled']}")

        # 2. Drive: Proactive task triggering
        state = await workspace.get_current_state.remote()
        entropy = drives.evaluate_state(state)
        print(f"[Hub] System Entropy: {entropy:.4f}")

        if entropy > config['drive_engine']['entropy_threshold']:
            print("[Drives] High Entropy detected. Triggering proactive tasks.")
            if tick % 2 == 0:
                await hub.safe_delegate(reasoner, "query", "math.factorial(6)")
            else:
                await hub.safe_delegate(coder, "code_execution", "print('Proactive self-test')")

        # 3. Process Scheduler Queue
        task = await scheduler.next.remote()
        if task:
            priority, handle, msg = task
            if handle:
                print(f"[Hub] Processing scheduled task: {msg['type']}")
                await handle.receive.remote(msg)

        await asyncio.sleep(1)

    print(f"\n{config['system_identity']['name']} Demo complete.")

if __name__ == "__main__":
    asyncio.run(cognitive_cycle())
