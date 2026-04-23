import concurrent.futures
import ray
from core.base import CognitiveModule

@ray.remote
class ConcurrencyManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)

    def run_parallel(self, agents, input_data):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(a.act, input_data): a for a in agents}
            return [f.result() for f in futures]

    def receive(self, message):
        """Standard SGI message receiver."""
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "parallel_execution":
            result = self.run_parallel(message["data"]["agents"], message["data"]["input"])
            self.send_result("parallel_result", result)
