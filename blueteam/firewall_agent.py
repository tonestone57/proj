Based on ELISAR Next-Gen Firewall, which performs real-time detection and adaptive filtering Springer.
class FirewallAgent:
    def filter(self, packet):
        if "malicious" in packet:
            return {"blocked": True}
        return {"blocked": False}