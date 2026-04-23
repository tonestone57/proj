from core.base import CognitiveModule
class FirewallAgent(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.rules = []

    def add_rule(self, pattern, action="block"):
        self.rules.append({"pattern": pattern, "action": action})

    def filter(self, packet):
        # Default policy: allow
        for rule in self.rules:
            if rule["pattern"] in str(packet):
                return {"blocked": rule["action"] == "block", "rule": rule["pattern"]}

        if "malicious" in str(packet):
            return {"blocked": True, "rule": "default_malicious_filter"}
        return {"blocked": False}

    def receive(self, message):
        """Standard SGI message receiver."""
        if message["type"] == "add_firewall_rule":
            self.add_rule(message["data"]["pattern"], message["data"].get("action", "block"))
