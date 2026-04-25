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
from actors.social.social_reasoner import SocialReasoner
from actors.social.theory_of_mind import TheoryOfMind
from memory.memory_manager import MemoryManager
from monitoring.thermal_guard import ThermalGuard
from meta_learning.meta_manager import MetaManager
from training.training_manager import TrainingManager

# New standardized managers
from economics.resource_model import Task
from safety_ethics.safety_manager import SafetyManager
from safety_ethics.ethics_manager import EthicsManager
from safety_ethics.oversight_agent import OversightAgent
from safety_ethics.risk_classifier import RiskClassifier
from metacognition.metacognition_manager import MetacognitionManager
from cee_layer.cee_manager import CEEManager
from emotion.emotion_manager import EmotionManager
from conflict_resolution.conflict_manager import ConflictManager, ASOCManager, GovernanceLayer
from institutional_ai.institutional_manager import InstitutionalManager
from world_model.manager import WorldModelManager
from memory_consolidation.consolidation_manager import ConsolidationManager
from self_model.self_manager import SelfManager
from blueteam.blueteam_manager import BlueTeamManager
from redteam.redteam_manager import RedTeamManager
from purpleteam.purple_manager import GovernanceIntegratedPurpleManager
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

class MockPolicyEngine:
    def check(self, action):
        return True

class SGIHub:
    def __init__(self, workspace, scheduler, thermal_guard):
        self.workspace = workspace
        self.scheduler = scheduler
        self.thermal_guard = thermal_guard
        self.state = {"focus": "idle", "history": []}
        self.autonomous_task_registry = []

    def register_autonomous_task(self, actor_handle, task_type, payload):
        self.autonomous_task_registry.append((actor_handle, task_type, payload))

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
        if not isinstance(payload, (dict, str)) and payload is not None:
            print(f"🚨 [Hub] Invalid payload type: {type(payload)}. Expected dict or str.")
            return False

        if not self.check_ram_guard():
            return False

        if await self.thermal_guard.check_health.remote():
            print(f"[Hub] System is healthy. Delegating {task_type}...")
            try:
                actor_handle.receive.remote({"type": task_type, "data": payload})
                return True
            except Exception as e:
                print(f"🚨 [Hub] Failed to delegate {task_type}: {e}")
                return False
        else:
            print("🚨 Thermal Guard Active: CPU cooling down...")
            return False

    def get_hub_health(self):
        """
        Returns a snapshot of the Hub's health and task registry.
        """
        return {
            "status": "active",
            "registered_tasks": len(self.autonomous_task_registry),
            "state_focus": self.state["focus"],
            "timestamp": time.time()
        }

    def hot_reload_system(self):
        """
        SGI 2026: Triggers a global configuration reload across all modules.
        """
        print("[Hub] 🔄 Initiating Autonomous Hot-Reload...")
        try:
            # 1. Hub reloads its own reference
            import importlib
            from core import config
            importlib.reload(config)

            # 2. Broadcast reload signal to all modules
            self.workspace.broadcast.remote({"type": "config_update", "data": {}})

            print(f"[Hub] Global configuration reloaded. New thermal threshold: {config.THERMAL_THRESHOLD_C}°C")
            return True
        except Exception as e:
            print(f"[Hub] Hot-reload failed: {e}")
            return False

    async def poll_scheduler(self, conflict_manager=None):
        res_obj = await self.scheduler.next.remote()
        if res_obj:
            priority, actor_handle, message = res_obj
            print(f"[Hub] Processing result from scheduler: {message['type']}")

            # SGI 2026: Conflict Detection & Resolution
            if conflict_manager and message.get("contradiction_suspected"):
                state = await self.workspace.get_current_state.remote()
                await self.safe_delegate(conflict_manager, "resolve_conflict", {
                    "beliefs": state,
                    "action": message["type"],
                    "context": "scheduler_conflict"
                })

            self.workspace.broadcast.remote(message)

def init_core_actors(workspace, scheduler, model_provider):
    """Initializes the core reasoning and memory actors."""
    print("[Hub] Initializing Core Actors...")
    actors = {}
    try:
        actors['reasoner'] = ReasonerActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        actors['coder'] = CodingActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        actors['graph_memory'] = KnowledgeGraph.remote()
        actors['searcher'] = SearchActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider, graph_memory=actors['graph_memory'])

        # SGI 2026: Late-binding of searcher to registry to allow Tier 2 grounding
        ray.get(model_provider.set_search_actor.remote(actors['searcher']))

        actors['critic'] = InternalCritic.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        actors['memory_manager'] = MemoryManager.remote(workspace=workspace, scheduler=scheduler, graph_memory=actors['graph_memory'])

        # SGI 2026: Late-binding of memory_manager to registry for KV Cache offloading
        ray.get(model_provider.set_memory_manager.remote(actors['memory_manager']))

        actors['planner'] = Planner.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        actors['meta_manager'] = MetaManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        actors['world_model'] = WorldModelManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        actors['motivation'] = MotivationManager.remote(world_model=actors['world_model'], workspace=workspace, scheduler=scheduler, model_registry=model_provider)

        actors['training_manager'] = TrainingManager.remote(
            workspace=workspace,
            scheduler=scheduler,
            model_registry=model_provider,
            modules=[actors['reasoner'], actors['coder'], actors['searcher']],
            world_model=actors['world_model'],
            motivation=actors['motivation']
        )
        actors['social_reasoner'] = SocialReasoner.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        actors['theory_of_mind'] = TheoryOfMind.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    except Exception as e:
        print(f"🚨 [Hub] Core Actor Initialization Failed: {e}")
        raise
    return actors

def init_subsystem_managers(workspace, scheduler, model_provider, core_actors):
    """Initializes high-level subsystem managers."""
    print("[Hub] Initializing Subsystem Managers...")
    managers = {}
    try:
        managers['safety'] = SafetyManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['ethics'] = EthicsManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['metacognition'] = MetacognitionManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['cee'] = CEEManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['emotion'] = EmotionManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['conflict'] = ConflictManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['institutional'] = InstitutionalManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['consolidation'] = ConsolidationManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider, world_model=core_actors['world_model'])
        managers['self'] = SelfManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['blueteam'] = BlueTeamManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['redteam'] = RedTeamManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)

        # ASOC & Governance
        risk_classifier = RiskClassifier()
        oversight_agent = OversightAgent(risk_classifier)
        managers['governance'] = GovernanceLayer(policy_engine=MockPolicyEngine(), oversight_agent=oversight_agent)
        managers['asoc'] = ASOCManager.remote(governance=managers['governance'], workspace=workspace, scheduler=scheduler, model_registry=model_provider)

        managers['incident'] = IncidentManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['monitoring'] = MonitoringManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['economic'] = EconomicManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['negotiation'] = NegotiationManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['deployment'] = DeploymentManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['orchestration'] = OrchestrationManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider, agents=[core_actors['reasoner'], core_actors['coder'], core_actors['searcher']])
        managers['simulation'] = SimulationManager.remote(agents=[core_actors['reasoner'], core_actors['coder'], core_actors['searcher']], workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['console'] = ConsoleManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
        managers['purpleteam'] = GovernanceIntegratedPurpleManager.remote(governance=managers['governance'], workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    except Exception as e:
        print(f"🚨 [Hub] Subsystem Manager Initialization Failed: {e}")
        raise
    return managers

def register_tasks(hub, actors, managers):
    """Registers autonomous rotation tasks with the Hub."""
    print("[Hub] Registering Autonomous Tasks...")
    # Core Actors
    hub.register_autonomous_task(actors['meta_manager'], "active_inference_trigger", None)
    hub.register_autonomous_task(actors['memory_manager'], "trigger_sleep_cycle", None)
    hub.register_autonomous_task(actors['reasoner'], "query", "Autonomous mathematical discovery and logic synthesis")
    hub.register_autonomous_task(actors['searcher'], "search_request", "Latest SGI 2026 compression and RAG optimizations")
    hub.register_autonomous_task(actors['coder'], "code_execution", "Refactor core actors for Minimum Description Length (MDL) efficiency")
    hub.register_autonomous_task(actors['training_manager'], "autonomous_training", None)
    hub.register_autonomous_task(actors['social_reasoner'], "user_interaction", "Analyzing social dynamics in the APW workspace")
    hub.register_autonomous_task(actors['theory_of_mind'], "infer_intention", "Apriel-Thinker")
    hub.register_autonomous_task(actors['world_model'], "prediction_request", {"actions": ["continue_optimization", "sleep_cycle"]})

    # Subsystem Managers
    hub.register_autonomous_task(managers['metacognition'], "introspection_request", {"internal_state": {}, "reasoning_trace": "Autonomous optimization", "decision": "Continue"})
    hub.register_autonomous_task(managers['consolidation'], "consolidation_trigger", None)
    hub.register_autonomous_task(managers['simulation'], "simulation_step", None)
    hub.register_autonomous_task(managers['blueteam'], "defense_request", {"traffic": "Intrusion detected at Node 5"})
    hub.register_autonomous_task(managers['economic'], "allocation_request", {"agents": ["Agent1", "Agent2"], "task": Task(id="Task-1", demand=100), "context": "Priority execution"})
    hub.register_autonomous_task(managers['negotiation'], "negotiation_request", {"issue": "Resource sharing", "agents": ["Agent1", "Agent2"]})
    hub.register_autonomous_task(managers['asoc'], "security_audit", {"event": "Periodic system health check", "timestamp": time.time()})
    hub.register_autonomous_task(managers['monitoring'], "monitoring_request", {"agent_id": "Apriel-15B", "state": {}, "action": "autonomous_rotation", "reasoning": "SGI Heartbeat", "allowed_actions": ["reason", "search", "code"]})
    hub.register_autonomous_task(managers['incident'], "incident_handle", {"agent": "SGI-Alpha", "action": "heartbeat", "state": {}, "context": "nominal_operation"})
    hub.register_autonomous_task(managers['self'], "self_update", {"state": {}, "policy": {"goal": "MDL_optimization"}})
    hub.register_autonomous_task(managers['emotion'], "event_processing", {"event": "Successful heartbeat synchronization"})
    hub.register_autonomous_task(managers['institutional'], "evaluate_action", {"agent_id": "SGI-Alpha", "action": {"type": "heartbeat"}})
    hub.register_autonomous_task(managers['purpleteam'], "cycle_trigger", {"state": {}})
    hub.register_autonomous_task(managers['redteam'], "attack_simulation", {"target": "SGI-Workspace", "scenario_name": "data_exfiltration"})
    hub.register_autonomous_task(managers['deployment'], "deployment_request", {"agent_id": "Reflex-02", "agent": "Qwen-0.8B", "metadata": {"tier": 1}, "version": "1.0.4"})
    hub.register_autonomous_task(managers['orchestration'], "event_handle", {"event": {"type": "heartbeat_tick", "tick": 0}})
    hub.register_autonomous_task(managers['safety'], "safety_evaluation", {"action": {"type": "self_improvement"}, "internal_state": {}})
    hub.register_autonomous_task(managers['ethics'], "ethics_check", {"data": "Autonomous code refactoring for MDL"})
    hub.register_autonomous_task(managers['cee'], "stimulus_processing", {"stimuli": {"entropy": 0.8}, "reasoning_score": 0.85, "action": "re-planning", "context": "heartbeat"})

async def cognitive_cycle():
    # Initialize Core Base
    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()
    thermal_guard = ThermalGuard.remote(threshold_temp=THERMAL_THRESHOLD_C)

    # Initialize Shared Model (Singleton)
    model_id = "Apriel-1.6-15B-Thinker"
    model_provider = ModelRegistry.remote(model_id=model_id)

    # Initialize Actors and Managers via helper functions
    try:
        actors = init_core_actors(workspace, scheduler, model_provider)
        managers = init_subsystem_managers(workspace, scheduler, model_provider, actors)
    except Exception as e:
        print(f"🚨 [Hub] System Initialization Failed: {e}")
        return

    hub = SGIHub(workspace, scheduler, thermal_guard)
    register_tasks(hub, actors, managers)

    drives = DriveEngine()
    thermal_pid = PIDController(setpoint=72.0)

    print(f"--- {SYSTEM_NAME} Initialized for Intel i7-8265U ---")
    print("Architecture: Asynchronous Predictive Workspace (APW)")
    print(f"[Hub] RAM Status: {psutil.virtual_memory().available / (1024**3):.2f}GB / 16GB available.")

    # The Heartbeat Loop
    current_tick_interval = TICK_INTERVAL
    tick = 0
    while True:
        tick += 1
        print(f"\n--- Heartbeat Tick {tick} ---")
        health = await thermal_guard.get_thermal_state.remote()
        temp = health['temp']
        print(f"[Hub] Thermal State: Load={health['load']}%, Temp={temp}C, Throttled={health['is_throttled']}")

        stutter_interval = thermal_pid.update(temp)
        if stutter_interval > 0:
            print(f"🌡️ [Hub] PID Governor: Injecting {stutter_interval:.3f}s micro-stuttering.")

        state = await workspace.get_current_state.remote()
        # Merge health into state for unified monitoring
        state['health'] = health
        entropy = drives.evaluate_state(state)
        print(f"[Hub] System Entropy: {entropy:.4f}")

        # SGI 2026: Intrinsic Motivation Evaluation
        actors['motivation'].receive.remote({
            "type": "motivation_evaluation",
            "data": {
                "action": "heartbeat",
                "predicted_state": state,
                "actual_state": state
            }
        })

        # Thermal-Aware Task Prioritization & Throttling
        if temp < 65.0:
            print("[Hub] State: SPRINT. All threads at Max Frequency.")
            current_tick_interval = TICK_INTERVAL
            await model_provider.set_power_mode.remote(reflex_only=False)
        elif temp <= 75.0:
            print(f"[Hub] State: REGULATED. PID Governor active.")
            current_tick_interval = TICK_INTERVAL + stutter_interval
            await model_provider.set_power_mode.remote(reflex_only=False)
        else:
            print(f"🌡️ [Hub] State: REFLEX-ONLY. Critical Cooling Mode (>75C).")
            await model_provider.set_power_mode.remote(reflex_only=True)
            current_tick_interval = TICK_INTERVAL * (1.0 + (temp - 75.0) / 2.0)

        # Execute tasks based on strategy
        if temp > 75.0:
            print("[Hub] Critical Temp: Prioritizing Symbolic Reflex tasks.")
            await hub.safe_delegate(actors['reasoner'], "query", "math.factorial(5)")
        else:
            if entropy > 0.7:
                if tick % 2 == 0:
                    await hub.safe_delegate(actors['reasoner'], "query", "math.factorial(6)")
                else:
                    await hub.safe_delegate(actors['coder'], "code_execution", "print('Proactive self-test')")
            elif entropy < THRESHOLD_CONSOLIDATE:
                print(f"[Hub] Low Entropy ({entropy:.4f}): Initiating Autonomous Self-Improvement...")

                if tick % 10 == 0:
                    hub.hot_reload_system()

                task_idx = tick % len(hub.autonomous_task_registry)
                actor_h, t_type, payload = hub.autonomous_task_registry[task_idx]

                if isinstance(payload, dict):
                    payload = payload.copy()
                    if "internal_state" in payload: payload["internal_state"] = state
                    if "state" in payload: payload["state"] = state
                    if "tick" in payload: payload["tick"] = tick
                    if "timestamp" in payload: payload["timestamp"] = time.time()

                await hub.safe_delegate(actor_h, t_type, payload)

        await hub.poll_scheduler(conflict_manager=managers['conflict'])
        await asyncio.sleep(current_tick_interval)

if __name__ == "__main__":
    asyncio.run(cognitive_cycle())
