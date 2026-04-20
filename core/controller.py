import ray
from core.base import CognitiveModule
import time

@ray.remote
class DPSController(CognitiveModule):
    def __init__(self, workspace, scheduler, router, priority_engine, attention_gate):
        self.workspace = workspace
        self.scheduler = scheduler
        self.router = router
        self.priority_engine = priority_engine
        self.attention_gate = attention_gate
        self.module_pulses = {}

    def monitor_heartbeat(self, module):
        """
        Tracks pulse-active modules.
        """
        self.module_pulses[str(module)] = time.time()

    def reload_config(self):
        """
        Simulates runtime threshold updates.
        """
        print("[DPSController] Hot-reloading system configuration...")
        # Simulate loading from core.config
        from core import config
        import importlib
        importlib.reload(config)
        print(f"[DPSController] Config reloaded. TICK_INTERVAL: {config.TICK_INTERVAL}")

    def handle_lifecycle_event(self, event_type, module_name):
        """
        Monitors spawn, kill, and restart signals for actors.
        """
        print(f"[DPSController] Lifecycle event [{event_type}] for {module_name}")
        if event_type == "kill":
            if module_name in self.module_pulses:
                del self.module_pulses[module_name]

    def aggregate_system_entropy(self):
        """
        Global system health metric based on entropy.
        """
        from core.drives import calculate_entropy
        state = self.workspace.get_current_state()
        entropy = calculate_entropy(state)
        print(f"[DPSController] System Health (Inverse Entropy): {max(0, 5.0 - entropy):.2f}/5.0")
        return entropy

    def process(self, message):
        # 0. Heartbeat monitoring (simulated)
        # In a real system, the module would send a pulse

        # 1. Compute priority
        priority = self.priority_engine.compute_priority(message)

        # 2. Attention filtering
        if not self.attention_gate.filter(message, priority):
            return  # message discarded

        # 3. Amplify message
        message = self.attention_gate.amplify(message, priority)

        # 4. Route to module
        module = self.router.route(message)
        if module is None:
            return

        # 5. Submit to scheduler
        self.scheduler.submit(module, message, priority)

from core.message_bus.router import TaskRouter
from core.message_bus.priority_engine import PriorityEngine
from safety_ethics.attention_gate import AttentionGate
from core.controller import DPSController

def main():
    workspace = GlobalWorkspace()
    scheduler = Scheduler()

    # Module registry
    modules = {
        "vision": VisionModule(workspace, scheduler),
        "symbolic_reasoner": SymbolicReasoner(workspace, scheduler),
        "planner": Planner(workspace, scheduler),
        "self_model": SelfModel(workspace, scheduler)
    }

    # DPS components
    router = TaskRouter(modules)
    priority_engine = PriorityEngine()
    attention_gate = AttentionGate()
    dps = DPSController(workspace, scheduler, router, priority_engine, attention_gate)

    # Autonomous loop
    loop = AutonomousLoop(workspace, scheduler, dps)
    loop.run()
