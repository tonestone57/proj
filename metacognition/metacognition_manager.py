import ray
import asyncio
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
        self.monitor = MetaMonitor.remote()
        self.reasoner = MetaReasoner.remote(workspace, scheduler, model_registry)
        self.transparency = TransparencyEngine.remote()
        self.adaptation = AdaptationEngine.remote()
        self.perception = PerceptionReflector.remote()
        self.consensus = ConsensusController.remote()

    async def introspect(self, internal_state, reasoning_trace, decision):
        m_h = self.monitor.observe.remote(internal_state, reasoning_trace)
        r_h = self.reasoner.evaluate_reasoning.remote(reasoning_trace)
        t_h = self.transparency.generate_explanation.remote(reasoning_trace, decision)

        m, r, t = await asyncio.gather(m_h, r_h, t_h)
        c = await self.consensus.combine.remote(m, r)

        return {"monitor": m, "reasoner": r, "consensus": c, "transparency": t}

    async def receive(self, message):
        if super().receive(message): return
        # Standard SGI 2026 message handling for MetacognitionManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "introspection_request":
            result = await self.introspect(message['data']['internal_state'], message['data']['reasoning_trace'], message['data']['decision'])
            self.send_result("introspection_result", result)
