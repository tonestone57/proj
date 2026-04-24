import ray
from core.base import CognitiveModule

@ray.remote
class CyberRange(CognitiveModule):
    def simulate_traffic(self):
        return ["normal", "suspicious", "malicious"]
