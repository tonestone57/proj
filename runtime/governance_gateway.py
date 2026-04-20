import ray
from core.base import CognitiveModule
@ray.remote
class GovernanceGateway(CognitiveModule):
    def __init__(self, governance_layer):
        self.gov = governance_layer

    def authorize(self, action):
        return self.gov.authorize(action)

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
