class FirewallAgent:
    def filter(self, packet):
        if "malicious" in packet:
            return {"blocked": True}
        return {"blocked": False}
