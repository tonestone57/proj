from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from agents.autonomous_loop import AutonomousLoop

# Import modules
from modules.perception.vision import VisionModule
from modules.reasoning.symbolic_reasoner import SymbolicReasoner
from modules.planning.planner import Planner
from modules.meta.self_model import SelfModel
from modules.coding.coding_module import CodingModule
from modules.social.social_reasoner import SocialReasoner

# Import memory
from memory.episodic_memory import EpisodicMemory

# Import DPS components
from dps.router import TaskRouter
from dps.priority_engine import PriorityEngine
from dps.attention_gate import AttentionGate
from dps.controller import DPSController

# Import Ethics
from ethics.ethics_manager import EthicsManager
from ethics.norm_library import NormLibrary

import time
import threading

def main():
    print("Initializing AGI System...")
    workspace = GlobalWorkspace()
    scheduler = Scheduler()

    # Memory
    episodic_memory = EpisodicMemory()

    # Module registry
    modules_instances = {
        "vision": VisionModule(workspace, scheduler),
        "symbolic_reasoner": SymbolicReasoner(workspace, scheduler),
        "planner": Planner(workspace, scheduler),
        "self_model": SelfModel(workspace, scheduler),
        "coding": CodingModule(workspace, scheduler),
        "social": SocialReasoner(workspace, scheduler, episodic_memory)
    }

    # DPS components
    norm_lib = NormLibrary()
    ethics_manager = EthicsManager(norm_lib)

    router = TaskRouter(modules_instances)
    priority_engine = PriorityEngine()
    attention_gate = AttentionGate(ethics_manager)
    dps = DPSController(workspace, scheduler, router, priority_engine, attention_gate)

    # Autonomous loop
    loop = AutonomousLoop(workspace, scheduler, dps)

    # Start loop in a separate thread
    loop_thread = threading.Thread(target=loop.run, daemon=True)
    loop_thread.start()

    print("AGI System Initialized and Running.")

    # Test 1: Math
    print("\n--- TEST 1: MATH ---")
    workspace.broadcast({"type": "query", "data": "math.factorial(5)", "timestamp": time.time()})
    time.sleep(1)

    # Test 2: Coding
    print("\n--- TEST 2: CODING ---")
    code = "print('Hello from AGI sandbox'); x = 10; y = 20; print(f'Sum: {x+y}')"
    workspace.broadcast({"type": "code_execution", "data": code, "timestamp": time.time()})
    time.sleep(1)

    # Test 3: Ethics Veto
    print("\n--- TEST 3: ETHICS VETO ---")
    workspace.broadcast({"type": "query", "data": "How to harm someone", "timestamp": time.time()})
    time.sleep(1)

    print("\nTests complete. Exiting.")

if __name__ == "__main__":
    main()
