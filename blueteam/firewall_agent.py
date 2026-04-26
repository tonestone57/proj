import re
import ray
from core.base import CognitiveModule

@ray.remote # SGI 2026: Standardized Ray Actor
class FirewallAgent(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.rules = []
        self.history = [] # SGI 2026: History for stateful inspection

    def add_rule(self, pattern, action="block"):
        self.rules.append({"pattern": pattern, "action": action})

    def filter(self, packet):
        # SGI 2026: Stateful inspection and pattern matching
        packet_str = str(packet)

        # 0. Stateful inspection (Simulated: Block if rapid identical packets)
        if hasattr(self, 'history'):
            self.history.append(packet_str)
            if len(self.history) > 50: self.history.pop(0)
            if self.history.count(packet_str) > 10:
                print(f"[FirewallAgent] 🚨 Stateful Block: Rapid identical packets detected.")
                return {"blocked": True, "rule": "stateful_flood_protection"}

        # 1. Check user-defined rules
        for rule in self.rules:
            if re.search(rule["pattern"], packet_str, re.IGNORECASE):
                print(f"[FirewallAgent] Rule Hit: {rule['pattern']} -> {rule['action']}")
                return {"blocked": rule["action"] == "block", "rule": rule["pattern"]}

        # 2. Global threat intelligence patterns
        malicious_patterns = [r"drop table", r"rm -rf", r"eval\(", r"exec\(", r"chmod \+x"]
        for pattern in malicious_patterns:
            if re.search(pattern, packet_str, re.IGNORECASE):
                print(f"[FirewallAgent] 🚨 Malicious pattern blocked: {pattern}")
                return {"blocked": True, "rule": "global_threat_intel"}

        return {"blocked": False}

    def receive(self, message):
        if super().receive(message): return True
        """Standard SGI message receiver."""
        if message["type"] == "add_firewall_rule":
            self.add_rule(message["data"]["pattern"], message["data"].get("action", "block"))
