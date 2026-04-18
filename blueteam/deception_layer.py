class DeceptionLayer:
    def deploy_honeypot(self, ip):
        return {"honeypot_active": True, "target_ip": ip}
