import ray
import time
import asyncio
import os
import psutil

# Core components
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from core.drives import DriveEngine
from core.config import CPU_CORES_MAX, MAX_THREADS, TICK_INTERVAL, SYSTEM_NAME, THERMAL_THRESHOLD_C, LOW_MEMORY_THRESHOLD_MB
from core.model_registry import ModelRegistry

# Actors
from actors.reasoner_actor import ReasonerActor
from actors.coding_actor import CodingActor
from actors.search_actor import SearchActor
from actors.critic_actor import InternalCritic
from actors.planner import Planner
from memory.memory_manager import MemoryManager
from monitoring.thermal_guard import ThermalGuard

# Enforce thread limits for Intel i7-8265U (15W TDP)
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

    def check_ram_guard(self):
        """
        Proactive RAM Guard to prevent swap lag and system crash.
        Threshold: 2000MB (Configured for 16GB system).
        """
        mem = psutil.virtual_memory()
        available_mb = mem.available / (1024 * 1024)
        if available_mb < LOW_MEMORY_THRESHOLD_MB:
            print(f"🚨 [RAM Guard] Critical memory pressure: {available_mb:.2f}MB available. Pausing ingestion.")
            return False
        return True

    async def safe_delegate(self, actor_handle, task_type, payload):
        if not self.check_ram_guard():
            return False

        if await self.thermal_guard.check_health.remote():
            print(f"[Hub] System is healthy. Delegating {task_type}...")
            actor_handle.receive.remote({"type": task_type, "data": payload})
            return True
        else:
            print("🚨 Thermal Guard Active: CPU cooling down...")
            return False

    async def poll_scheduler(self):
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

    # Initialize Shared Model (Singleton) to prevent RAM crash
    model_id = "DeepSeek-Coder-V2-Lite"
    model_provider = ModelRegistry.remote(model_id=model_id)

    # Initialize Specialized Actors using the shared model provider
    reasoner = ReasonerActor.remote(workspace, scheduler, model_registry=model_provider)
    coder = CodingActor.remote(workspace, scheduler, model_registry=model_provider)
    searcher = SearchActor.remote(workspace, scheduler, model_registry=model_provider)
    critic = InternalCritic.remote(workspace, scheduler, model_registry=model_provider)
    planner = Planner.remote(workspace, scheduler, model_registry=model_provider)
    memory_manager = MemoryManager.remote(workspace, scheduler)

    hub = SGIHub(workspace, scheduler, thermal_guard)
    drives = DriveEngine()

    print(f"--- {SYSTEM_NAME} Initialized for Intel i7-8265U ---")
    print("Architecture: Asynchronous Predictive Workspace (APW)")
    print(f"[Hub] RAM Status: {psutil.virtual_memory().available / (1024**3):.2f}GB / 16GB available.")

    # The Heartbeat Loop
    for tick in range(10):
        print(f"\n--- Heartbeat Tick {tick+1} ---")
        health = await thermal_guard.get_thermal_state.remote()
        print(f"[Hub] Thermal State: Load={health['load']}%, Temp={health['temp']}C, Throttled={health['is_throttled']}")

        state = await workspace.get_current_state.remote()
        entropy = drives.evaluate_state(state)
        print(f"[Hub] System Entropy: {entropy:.4f}")

        if entropy > 0.7:
            if tick % 2 == 0:
                await hub.safe_delegate(reasoner, "query", "math.factorial(6)")
            else:
                await hub.safe_delegate(coder, "code_execution", "print('Proactive self-test')")

        await hub.poll_scheduler()
        await asyncio.sleep(TICK_INTERVAL)

    print(f"\n{SYSTEM_NAME} Demo complete.")

if __name__ == "__main__":
    asyncio.run(cognitive_cycle())
