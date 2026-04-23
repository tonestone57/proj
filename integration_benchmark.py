import asyncio
import ray
import time
import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from main import cognitive_cycle, SGIHub
from core.config import TICK_INTERVAL

async def run_integration_benchmark(ticks=10):
    print(f"🚀 Starting SGI Integration Benchmark for {ticks} ticks...")

    # We'll use a modified version of cognitive_cycle logic that stops after N ticks
    # Since cognitive_cycle in main.py has an infinite loop, we'll implement a testable variant here

    from core.workspace import GlobalWorkspace
    from core.scheduler import Scheduler
    from monitoring.thermal_guard import ThermalGuard
    from core.model_registry import ModelRegistry
    from actors.reasoner_actor import ReasonerActor
    from actors.coding_actor import CodingActor
    from actors.search_actor import SearchActor
    from memory.long_term.graph_memory import KnowledgeGraph

    ray.init(ignore_reinit_error=True)

    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()
    from core.config import SGI_SETTINGS
    thermal_guard = ThermalGuard.remote(threshold_temp=80.0)
    graph_memory = KnowledgeGraph.remote()
    model_provider = ModelRegistry.remote(model_id=SGI_SETTINGS.inference.primary_model)

    reasoner = ReasonerActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    coder = CodingActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    searcher = SearchActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider, graph_memory=graph_memory)

    hub = SGIHub(workspace, scheduler, thermal_guard)
    hub.register_autonomous_task(reasoner, "query", "Integration Test Query")
    hub.register_autonomous_task(coder, "code_execution", "print('Integration Test')")

    print("[Benchmark] Hub initialized. Starting loop...")

    for i in range(1, ticks + 1):
        print(f"\n--- Benchmark Tick {i} ---")
        health = await thermal_guard.get_thermal_state.remote()
        print(f"[Benchmark] Health: {health}")

        # Simulate task delegation
        task_idx = i % len(hub.autonomous_task_registry)
        actor, t_type, payload = hub.autonomous_task_registry[task_idx]
        await hub.safe_delegate(actor, t_type, payload)

        # Poll scheduler
        await hub.poll_scheduler()

        await asyncio.sleep(0.1) # Fast tick for benchmark

    print("\n✅ Integration Benchmark Completed Successfully")
    ray.shutdown()

if __name__ == "__main__":
    asyncio.run(run_integration_benchmark())
