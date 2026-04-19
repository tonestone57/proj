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
from core.heartbeat import CognitiveHeartbeat

# Actors
from actors.reasoner_actor import ReasonerActor
from actors.coding_actor import CodingActor
from actors.search_actor import SearchActor
from actors.critic_actor import InternalCritic
from actors.planner import Planner
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
            result = await actor_handle.receive.remote({"type": task_type, "data": payload})
            if result:
                await self.workspace.broadcast.remote(result)
            return result
        else:
            print("🚨 Thermal Guard Active: CPU cooling down...")
            await asyncio.sleep(5)
            return "Task delayed due to thermal pressure."

async def cognitive_cycle():
    # Initialize Core Actors
    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()
    thermal_guard = ThermalGuard.remote(threshold_temp=config['hardware_limits']['thermal_threshold_celsius'])

    # Initialize Specialized Actors
    model_id = "intel/neural-chat-14b-v3-3"
    reasoner = ReasonerActor.remote(workspace, scheduler, model_id=model_id)
    coder = CodingActor.remote(workspace, scheduler, model_id=model_id)
    searcher = SearchActor.remote(workspace, scheduler, model_id=model_id)
    critic = InternalCritic.remote(workspace, scheduler, model_id=model_id)
    planner = Planner.remote(workspace, scheduler)
    memory_manager = MemoryManager.remote(workspace, scheduler)

    # Register subscribers to workspace
    await workspace.register.remote(reasoner)
    await workspace.register.remote(coder)
    await workspace.register.remote(searcher)
    await workspace.register.remote(critic)
    await workspace.register.remote(planner)
    await workspace.register.remote(memory_manager)

    hub = SGIHub(workspace, scheduler, thermal_guard)
    heartbeat = CognitiveHeartbeat(workspace, scheduler, planner=planner, memory_manager=memory_manager)

    print(f"--- {config['system_identity']['name']} Initialized for Intel i5-8265U ---")
    print(f"Mode: {config['system_identity']['mode']}")

    # The Heartbeat Loop
    for tick in range(5):
        print(f"\n--- Heartbeat Tick {tick+1} ---")

        # 1. Check health
        health = await thermal_guard.get_thermal_state.remote()
        print(f"[Hub] Thermal State: Load={health['load']}%, Temp Throttled={health['is_throttled']}")

        # 2. Heartbeat: entropy and proactive tasks
        await heartbeat.heartbeat_tick()

        # 3. Manual proactive triggers for demo if needed
        # (Usually handled by heartbeat/entropy, but we can add some here)
        if tick % 2 == 0:
            await hub.safe_delegate(reasoner, "query", "math.factorial(6)")

        # 4. Process Scheduler Queue
        task = await scheduler.next.remote()
        if task:
            priority, handle, msg = task
            if handle:
                print(f"[Hub] Processing scheduled task: {msg['type']}")
                result = await handle.receive.remote(msg)
                if result:
                    await self.workspace.broadcast.remote(result)

        await asyncio.sleep(1)

    print(f"\n{config['system_identity']['name']} Demo complete.")

if __name__ == "__main__":
    asyncio.run(cognitive_cycle())
