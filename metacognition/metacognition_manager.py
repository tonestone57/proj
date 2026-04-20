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
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.monitor = MetaMonitor()
        self.reasoner = MetaReasoner()
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
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
