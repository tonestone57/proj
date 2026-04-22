import ray
import time
import asyncio
import os
import psutil

# Core components
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from core.drives import DriveEngine, PIDController
from core.config import (
    CPU_CORES_MAX, MAX_THREADS, TICK_INTERVAL, SYSTEM_NAME,
    THERMAL_THRESHOLD_C, LOW_MEMORY_THRESHOLD_MB, THRESHOLD_CONSOLIDATE
)
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
from meta_learning.meta_manager import MetaManager
from training.training_manager import TrainingManager

# New standardized managers
from economics.resource_model import Task
from safety_ethics.safety_manager import SafetyManager
from safety_ethics.ethics_manager import EthicsManager
from metacognition.metacognition_manager import MetacognitionManager
from cee_layer.cee_manager import CEEManager
from emotion.emotion_manager import EmotionManager
from conflict_resolution.conflict_manager import ConflictManager
from institutional_ai.institutional_manager import InstitutionalManager
from world_model.manager import WorldModelManager
from memory_consolidation.consolidation_manager import ConsolidationManager
from self_model.self_manager import SelfManager
from blueteam.blueteam_manager import BlueTeamManager
from redteam.redteam_manager import RedTeamManager
from purpleteam.purple_manager import PurpleManager
from incident_response.incident_manager import IncidentManager
from monitoring.monitoring_manager import MonitoringManager
from economics.economic_manager import EconomicManager
from negotiation.negotiation_manager import NegotiationManager
from deployment.deployment_manager import DeploymentManager
from orchestration.orchestration_manager import OrchestrationManager
from simulation.simulation_manager import SimulationManager
from console.console_manager import ConsoleManager
from motivation.motivation_manager import MotivationManager

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
    reasoner = ReasonerActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    coder = CodingActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    searcher = SearchActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider, graph_memory=graph_memory)
    critic = InternalCritic.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    planner = Planner.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    memory_manager = MemoryManager.remote(workspace=workspace, scheduler=scheduler, graph_memory=graph_memory)
    meta_manager = MetaManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    training_manager = TrainingManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)

    # Initialize New Managers
    safety_manager = SafetyManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    ethics_manager = EthicsManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    metacognition_manager = MetacognitionManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    cee_manager = CEEManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    emotion_manager = EmotionManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    conflict_manager = ConflictManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    institutional_manager = InstitutionalManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    world_model_manager = WorldModelManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    consolidation_manager = ConsolidationManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    self_manager = SelfManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    blueteam_manager = BlueTeamManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    redteam_manager = RedTeamManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    purpleteam_manager = PurpleManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    incident_manager = IncidentManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    monitoring_manager = MonitoringManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    economic_manager = EconomicManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    negotiation_manager = NegotiationManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    deployment_manager = DeploymentManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    orchestration_manager = OrchestrationManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    simulation_manager = SimulationManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    console_manager = ConsoleManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    motivation_manager = MotivationManager.remote(world_model=world_model_manager, workspace=workspace, scheduler=scheduler, model_registry=model_provider)

    hub = SGIHub(workspace, scheduler, thermal_guard)
    drives = DriveEngine()
    thermal_pid = PIDController(setpoint=72.0)

    print(f"--- {SYSTEM_NAME} Initialized for Intel i7-8265U ---")
    print("Architecture: Asynchronous Predictive Workspace (APW)")
    print(f"[Hub] RAM Status: {psutil.virtual_memory().available / (1024**3):.2f}GB / 16GB available.")

    # The Heartbeat Loop (Continuous Autonomous Operation)
    current_tick_interval = TICK_INTERVAL
    tick = 0
    while True:
        tick += 1
        print(f"\n--- Heartbeat Tick {tick} ---")
        health = await thermal_guard.get_thermal_state.remote()
        temp = health['temp']
        print(f"[Hub] Thermal State: Load={health['load']}%, Temp={temp}C, Throttled={health['is_throttled']}")

        # SGI 2026: PID-based Thermal Governor
        stutter_interval = thermal_pid.update(temp)
        if stutter_interval > 0:
            print(f"🌡️ [Hub] PID Governor: Injecting {stutter_interval:.3f}s micro-stuttering.")

        state = await workspace.get_current_state.remote()
        entropy = drives.evaluate_state(state)
        print(f"[Hub] System Entropy: {entropy:.4f}")

        # SGI 2026: Thermal-Aware Task Prioritization & Throttling (3-Tier Strategy)
        if temp < 65.0:
            # Tier 1: Sprint (< 65C)
            print("[Hub] State: SPRINT. All threads at Max Frequency.")
            current_tick_interval = TICK_INTERVAL
            await model_provider.set_power_mode.remote(reflex_only=False)
        elif temp <= 75.0:
            # Tier 2: Regulated (65C - 75C)
            # Duty cycle threads: 80% active, 20% wait simulated via PID stutter
            print(f"[Hub] State: REGULATED. PID Governor active.")
            current_tick_interval = TICK_INTERVAL + stutter_interval
            await model_provider.set_power_mode.remote(reflex_only=False)
        else:
            # Tier 3: Reflex-Only (> 75C)
            # Suspend Apriel-15B; only Qwen-0.8B (via ModelRegistry reflex mode) handles I/O.
            print(f"🌡️ [Hub] State: REFLEX-ONLY. Critical Cooling Mode (>75C).")
            await model_provider.set_power_mode.remote(reflex_only=True)
            current_tick_interval = TICK_INTERVAL * (1.0 + (temp - 75.0) / 2.0)

        # Execute tasks based on strategy
        if temp > 75.0:
            # Reflex-Only task prioritization
            print("[Hub] Critical Temp: Prioritizing Symbolic Reflex tasks.")
            await hub.safe_delegate(reasoner, "query", "math.factorial(5)")
        else:
            # Normal or Regulated prioritization
            if entropy > 0.7:
                if tick % 2 == 0:
                    await hub.safe_delegate(reasoner, "query", "math.factorial(6)")
                else:
                    await hub.safe_delegate(coder, "code_execution", "print('Proactive self-test')")
            elif entropy < THRESHOLD_CONSOLIDATE:
                # SGI 2026: Autonomous Self-Improvement Cycle
                print(f"[Hub] Low Entropy ({entropy:.4f}): Initiating Autonomous Self-Improvement...")

                # Cycle through autonomous tasks
                cycle_step = tick % 12
                if cycle_step == 0:
                    await hub.safe_delegate(meta_manager, "active_inference_trigger", None)
                elif cycle_step == 1:
                    await hub.safe_delegate(memory_manager, "trigger_sleep_cycle", None)
                elif cycle_step == 2:
                    await hub.safe_delegate(reasoner, "query", "Autonomous mathematical discovery and logic synthesis")
                elif cycle_step == 3:
                    await hub.safe_delegate(searcher, "search_request", "Latest SGI 2026 compression and RAG optimizations")
                elif cycle_step == 4:
                    await hub.safe_delegate(coder, "code_execution", "Refactor core actors for Minimum Description Length (MDL) efficiency")
                elif cycle_step == 5:
                    await hub.safe_delegate(training_manager, "autonomous_training", None)
                elif cycle_step == 6:
                    await hub.safe_delegate(metacognition_manager, "introspection_request", {"internal_state": state, "reasoning_trace": "Autonomous optimization", "decision": "Continue"})
                elif cycle_step == 7:
                    await hub.safe_delegate(consolidation_manager, "consolidation_trigger", None)
                elif cycle_step == 8:
                    await hub.safe_delegate(simulation_manager, "simulation_step", None)
                elif cycle_step == 9:
                    await hub.safe_delegate(blueteam_manager, "defense_request", {"traffic": "Intrusion detected at Node 5"})
                elif cycle_step == 10:
                    await hub.safe_delegate(economic_manager, "allocation_request", {"agents": ["Agent1", "Agent2"], "task": Task(id="Task-1", demand=100), "context": "Priority execution"})
                elif cycle_step == 11:
                    await hub.safe_delegate(negotiation_manager, "negotiation_request", {"issue": "Resource sharing", "agents": ["Agent1", "Agent2"]})

        await hub.poll_scheduler()
        await asyncio.sleep(current_tick_interval)

    print(f"\n{SYSTEM_NAME} Demo complete.")

if __name__ == "__main__":
    asyncio.run(cognitive_cycle())
