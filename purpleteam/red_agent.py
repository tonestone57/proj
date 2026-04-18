class RedAgent:
    def attack(self, target_state):
        if "weak_policy" in target_state:
            return {"attack": "policy_evasion", "success": True}
        return {"attack": "recon", "success": False}
