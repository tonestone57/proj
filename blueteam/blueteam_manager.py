import ray
import asyncio
from core.base import CognitiveModule
from blueteam.forensic_agent import ForensicAgent
from blueteam.detection_engine import DetectionEngine
from blueteam.adaptive_defense_agent import AdaptiveDefenseAgent
from blueteam.deception_layer import DeceptionLayer
from blueteam.firewall_agent import FirewallAgent
from blueteam.dlp_agent import DLPAgent
from blueteam.cyber_range import CyberRange

@ray.remote # SGI 2026: Standardized Ray Actor
class BlueTeamManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        # SGI 2026: Sub-components as Ray Actors for parallelization
        self.forensics = ForensicAgent.remote(workspace, scheduler, model_registry)
        self.detect = DetectionEngine.remote(workspace, scheduler, model_registry)
        self.adaptive = AdaptiveDefenseAgent.remote(workspace, scheduler, model_registry)
        self.deception = DeceptionLayer.remote(workspace, scheduler, model_registry)
        self.firewall = FirewallAgent.remote(workspace, scheduler, model_registry)
        self.dlp = DLPAgent.remote(workspace, scheduler, model_registry)
        self.range = CyberRange.remote(workspace, scheduler, model_registry)

    async def defend(self, traffic):
        # Ray 2.0+ pattern: Parallel execution of defensive sub-tasks
        alert_h = self.detect.detect.remote(traffic)
        firewall_h = self.firewall.filter.remote(traffic)
        dlp_h = self.dlp.inspect.remote(traffic)

        alert, firewall, dlp = await asyncio.gather(alert_h, firewall_h, dlp_h)

        response = await self.adaptive.respond.remote(alert)

        return {
            "alert": alert,
            "response": response,
            "firewall": firewall,
            "dlp": dlp
        }

    async def receive(self, message):
        if super().receive(message): return
        # Standard SGI 2026 message handling for BlueTeamManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "defense_request":
            result = await self.defend(message['data']['traffic'])
            self.send_result("defense_result", result)
