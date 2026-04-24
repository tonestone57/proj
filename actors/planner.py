import ray
from core.base import CognitiveModule

@ray.remote
class Planner(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        print(f"[Planner] Initialized with Shared Model Provider.")

    def receive(self, message):
        if super().receive(message): return

        if message["type"] == "goal":
            plan = self.create_plan(message["data"])
            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None
            self.scheduler.submit.remote(handle, {"type": "plan", "data": plan})

    def create_plan(self, goal):
        print(f"[Planner] Creating plan for goal: {goal}")
        if self.model_registry:
            # SGI 2026: Intelligent task decomposition via Shared Model Provider
            prompt = f"Decompose this goal into actionable tasks: {goal}"
            result = ray.get(self.model_registry.generate.remote(prompt))
            # Simulated parsing of LLM output
            return [f"Task 1 for {goal}", f"Task 2 for {goal}"]

        return ["Analyze Goal", "Execute Steps", "Verify Results"]