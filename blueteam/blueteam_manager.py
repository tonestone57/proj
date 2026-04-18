from blueteam.forensic_agent import ForensicAgent
from blueteam.detection_engine import DetectionEngine
from blueteam.adaptive_defense_agent import AdaptiveDefenseAgent
from blueteam.deception_layer import DeceptionLayer
from blueteam.firewall_agent import FirewallAgent
from blueteam.dlp_agent import DLPAagent
from blueteam.cyber_range import CyberRange

class BlueTeamManager:
    def __init__(self):
        self.forensics = ForensicAgent()
        self.detect = DetectionEngine()
        self.adaptive = AdaptiveDefenseAgent()
        self.deception = DeceptionLayer()
        self.firewall = FirewallAgent()
        self.dlp = DLPAagent()
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
