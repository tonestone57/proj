from metacognition.meta_monitor import MetaMonitor
from metacognition.meta_reasoner import MetaReasoner
from metacognition.transparency_engine import TransparencyEngine
from metacognition.adaptation_engine import AdaptationEngine
from metacognition.perception_reflector import PerceptionReflector
from metacognition.consensus_controller import ConsensusController

class MetacognitionManager:
    def __init__(self):
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
