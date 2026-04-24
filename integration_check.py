import asyncio
import ray
import time
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from core.model_registry import ModelRegistry
from core.config import TICK_INTERVAL

# Import all managers as done in main.py
from actors.reasoner_actor import ReasonerActor
from actors.coding_actor import CodingActor
from actors.search_actor import SearchActor
from actors.critic_actor import InternalCritic
from actors.planner import Planner
from memory.memory_manager import MemoryManager
from meta_learning.meta_manager import MetaManager
from training.training_manager import TrainingManager
from actors.social.social_reasoner import SocialReasoner
from actors.social.theory_of_mind import TheoryOfMind
from safety_ethics.safety_manager import SafetyManager
from safety_ethics.ethics_manager import EthicsManager
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
from safety_ethics.risk_classifier import RiskClassifier
from safety_ethics.oversight_agent import OversightAgent

class MockPolicyEngine:
    def check(self, action):
        return True

async def run_check():
    print("🚀 Starting SGI-Alpha Integration Check...")
    # Initialize Ray. Aggressive CPU count (16) is reduced for development stability.
    ray.init(ignore_reinit_error=True, num_cpus=8)

    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()

    # Warm up Ray and Scheduler
    print("Warming up Ray...")
    await asyncio.sleep(2)
    model_provider = ModelRegistry.remote(model_id="Apriel-1.6-15B-Thinker")

    # Wait for ModelRegistry to initialize (it can take time to fail stages)
    print("Waiting for ModelRegistry to stabilize...")
    await asyncio.sleep(10)

    # Initialize components that are dependencies for others
    world_model_manager = WorldModelManager.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider)
    motivation_manager = MotivationManager.remote(world_model=world_model_manager, workspace=workspace, scheduler=scheduler, model_registry=model_provider)

    # Governance for ASOC
    risk_classifier = RiskClassifier()
    oversight_agent = OversightAgent(risk_classifier)
    governance = GovernanceLayer(policy_engine=MockPolicyEngine(), oversight_agent=oversight_agent)

    managers = {
        "Reasoner": (ReasonerActor, {}),
        "Coder": (CodingActor, {}),
        "Searcher": (SearchActor, {"graph_memory": None, "memory_manager": None}),
        "Critic": (InternalCritic, {}),
        "Planner": (Planner, {}),
        "MemoryManager": (MemoryManager, {"graph_memory": None}),
        "MetaManager": (MetaManager, {}),
        "TrainingManager": (TrainingManager, {"world_model": world_model_manager, "motivation": motivation_manager}),
        "SocialReasoner": (SocialReasoner, {}),
        "TheoryOfMind": (TheoryOfMind, {}),
        "SafetyManager": (SafetyManager, {}),
        "EthicsManager": (EthicsManager, {}),
        "MetacognitionManager": (MetacognitionManager, {}),
        "CEEManager": (CEEManager, {}),
        "EmotionManager": (EmotionManager, {}),
        "ConflictManager": (ConflictManager, {}),
        "InstitutionalManager": (InstitutionalManager, {}),
        "WorldModelManager": (WorldModelManager, {}),
        "ConsolidationManager": (ConsolidationManager, {}),
        "SelfManager": (SelfManager, {}),
        "BlueTeamManager": (BlueTeamManager, {}),
        "RedTeamManager": (RedTeamManager, {}),
        "PurpleManager": (PurpleManager, {}),
        "IncidentManager": (IncidentManager, {}),
        "MonitoringManager": (MonitoringManager, {}),
        "EconomicManager": (EconomicManager, {}),
        "NegotiationManager": (NegotiationManager, {}),
        "DeploymentManager": (DeploymentManager, {}),
        "OrchestrationManager": (OrchestrationManager, {}),
        "SimulationManager": (SimulationManager, {}),
        "ConsoleManager": (ConsoleManager, {}),
        "MotivationManager": (MotivationManager, {"world_model": world_model_manager}),
        "ASOCManager": (ASOCManager, {"governance": governance})
    }

    results = {}

    for name, (cls, extra_args) in managers.items():
        print(f"Checking {name}...")
        try:
            # Re-initialize to avoid stale state if needed, but here we just instantiate once.
            handle = cls.remote(workspace=workspace, scheduler=scheduler, model_registry=model_provider, **extra_args)

            # Ping
            handle.receive.remote({"type": "ping", "data": {}})

            # Allow some time for processing
            res = None
            for _ in range(20): # Increased wait time
                await asyncio.sleep(0.5)
                res = await scheduler.next.remote()
                if res:
                    _, actor_h, msg = res
                    if msg["type"] == "pong":
                        results[name] = "OK"
                        break
                    else:
                        # Put it back if it's not our pong?
                        # Actually scheduler.next() pops. In a real system this would be a problem.
                        # For this check, we assume only we are using the scheduler.
                        print(f"[{name}] Unexpected msg type {msg['type']}")

            if name not in results:
                results[name] = "WARNING: No pong received"
        except Exception as e:
            results[name] = f"CRITICAL: {str(e)}"

    print("\n--- Integration Check Results ---")
    for name, status in sorted(results.items()):
        print(f"{name:20}: {status}")

    ray.shutdown()

if __name__ == "__main__":
    asyncio.run(run_check())
