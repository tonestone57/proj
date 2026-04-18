class DPSController:
    def __init__(self, workspace, scheduler, router, priority_engine, attention_gate):
        self.workspace = workspace
        self.scheduler = scheduler
        self.router = router
        self.priority_engine = priority_engine
        self.attention_gate = attention_gate

    def process(self, message):
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
