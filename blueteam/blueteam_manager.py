import ray
from core.base import CognitiveModule
from blueteam.forensic_agent import ForensicAgent
from blueteam.detection_engine import DetectionEngine
from blueteam.adaptive_defense_agent import AdaptiveDefenseAgent
from blueteam.deception_layer import DeceptionLayer
from blueteam.firewall_agent import FirewallAgent
from blueteam.dlp_agent import DLPAgent
from blueteam.cyber_range import CyberRange

@ray.remote
class BlueTeamManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.forensics = ForensicAgent()
        self.detect = DetectionEngine()
        self.adaptive = AdaptiveDefenseAgent()
        self.deception = DeceptionLayer()
        self.firewall = FirewallAgent()
        self.dlp = DLPAgent()
        self.range = CyberRange()

    def defend(self, traffic):
        alert = self.detect.detect(traffic)
        response = self.adaptive.respond(alert)
        firewall = self.firewall.filter(traffic)
        dlp = self.dlp.inspect(traffic)
        return {
            "alert": alert,
            "response": response,
            "firewall": firewall,
            "dlp": dlp
        }

    def receive(self, message):
        # Standard SGI 2026 message handling for BlueTeamManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "defense_request":
            result = self.defend(message['data']['traffic'])
            self.send_result("defense_result", result)
