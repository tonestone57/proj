from core.base import CognitiveModule
class FirewallAgent(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)

    def filter(self, packet):
        if "malicious" in packet:
            return {"blocked": True}
        return {"blocked": False}

    def receive(self, message):
        """Standard SGI message receiver."""
        pass
