import concurrent.futures
import ray
from core.base import CognitiveModule

@ray.remote
class ConcurrencyManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)

    def run_parallel(self, agents, input_data):
        """SGI 2026: Parallel execution of agent actions using Ray."""
        # Note: In a Ray environment, this should ideally use ray.get on multiple futures
        futures = [a.act.remote(input_data) for a in agents]
        return ray.get(futures)

    def receive(self, message):
        if super().receive(message): return
        """Standard SGI message receiver."""
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "parallel_execution":
            result = self.run_parallel(message["data"]["agents"], message["data"]["input"])
            self.send_result("parallel_result", result)
