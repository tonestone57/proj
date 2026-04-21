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
from memory.long_term.graph_memory import KnowledgeGraph
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
    graph_memory = KnowledgeGraph.remote()

    # Initialize Shared Model (Singleton) to prevent RAM crash
    model_id = "Apriel-1.6-15B-Thinker"
    model_provider = ModelRegistry.remote(model_id=model_id)

    # Initialize Specialized Actors using the shared model provider
    reasoner = ReasonerActor.remote(workspace, scheduler, model_registry=model_provider)
    coder = CodingActor.remote(workspace, scheduler, model_registry=model_provider)
    searcher = SearchActor.remote(workspace, scheduler, model_registry=model_provider, graph_memory=graph_memory)
    critic = InternalCritic.remote(workspace, scheduler, model_registry=model_provider)
    planner = Planner.remote(workspace, scheduler, model_registry=model_provider)
    memory_manager = MemoryManager.remote(workspace, scheduler, graph_memory=graph_memory)

    hub = SGIHub(workspace, scheduler, thermal_guard)
    drives = DriveEngine()

    print(f"--- {SYSTEM_NAME} Initialized for Intel i7-8265U ---")
    print("Architecture: Asynchronous Predictive Workspace (APW)")
    print(f"[Hub] RAM Status: {psutil.virtual_memory().available / (1024**3):.2f}GB / 16GB available.")

    # The Heartbeat Loop
    current_tick_interval = TICK_INTERVAL
    for tick in range(10):
        print(f"\n--- Heartbeat Tick {tick+1} ---")
        health = await thermal_guard.get_thermal_state.remote()
        print(f"[Hub] Thermal State: Load={health['load']}%, Temp={health['temp']}C, Throttled={health['is_throttled']}")

        state = await workspace.get_current_state.remote()
        entropy = drives.evaluate_state(state)
        print(f"[Hub] System Entropy: {entropy:.4f}")

        # SGI 2026: Thermal-Aware Task Prioritization & Throttling (Graduated)
        # We start throttling as we approach 80C (threshold set to 75C for proactive cooling)
        if health['temp'] > 75.0:
            print(f"🌡️ [Hub] Thermal Caution ({health['temp']}C)! Reducing CPU duty cycle.")

            # 1. Reduce 'CPU Speed' by increasing the heartbeat interval (Throttling)
            # Scaling delay based on how much we exceed 75C
            throttle_factor = 1.0 + (health['temp'] - 75.0) / 5.0
            current_tick_interval = TICK_INTERVAL * throttle_factor
            print(f"[Hub] Proactive Throttling: New Tick Interval = {current_tick_interval:.2f}s")

            # 2. Task Prioritization:
            # If > 80C, strictly force symbolic reflex to save TDP.
            # If 75-80C, mix in more symbolic tasks than usual.
            if health['temp'] > 80.0:
                print("[Hub] Critical Temp: Prioritizing Symbolic Reasoner exclusively.")
                await hub.safe_delegate(reasoner, "query", "math.factorial(5)")
            else:
                # Moderate heat: prioritize reasoner but allow some coding
                if tick % 3 == 0:
                    await hub.safe_delegate(coder, "code_execution", "print('Throttled Test')")
                else:
                    await hub.safe_delegate(reasoner, "query", "math.factorial(5)")
        else:
            current_tick_interval = TICK_INTERVAL
            if entropy > 0.7:
                if tick % 2 == 0:
                    await hub.safe_delegate(reasoner, "query", "math.factorial(6)")
                else:
                    await hub.safe_delegate(coder, "code_execution", "print('Proactive self-test')")

        await hub.poll_scheduler()
        await asyncio.sleep(current_tick_interval)

    print(f"\n{SYSTEM_NAME} Demo complete.")

if __name__ == "__main__":
    asyncio.run(cognitive_cycle())
