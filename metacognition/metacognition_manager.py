import ray
from core.base import CognitiveModule
from metacognition.meta_monitor import MetaMonitor
from metacognition.meta_reasoner import MetaReasoner
from metacognition.transparency_engine import TransparencyEngine
from metacognition.adaptation_engine import AdaptationEngine
from metacognition.perception_reflector import PerceptionReflector
from metacognition.consensus_controller import ConsensusController

@ray.remote
class MetacognitionManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.monitor = MetaMonitor()
        self.reasoner = MetaReasoner(workspace, scheduler, model_registry)
        self.transparency = TransparencyEngine()
        self.adaptation = AdaptationEngine()
        self.perception = PerceptionReflector()
        self.consensus = ConsensusController()

    def introspect(self, internal_state, reasoning_trace, decision):
        m = self.monitor.observe(internal_state, reasoning_trace)
        r = self.reasoner.evaluate_reasoning(reasoning_trace)
        c = self.consensus.combine(m, r)
        t = self.transparency.generate_explanation(reasoning_trace, decision)
        return {"monitor": m, "reasoner": r, "consensus": c, "transparency": t}

    def receive(self, message):
        # Standard SGI 2026 message handling for MetacognitionManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "introspection_request":
            result = self.introspect(message['data']['internal_state'], message['data']['reasoning_trace'], message['data']['decision'])
            self.send_result("introspection_result", result)
