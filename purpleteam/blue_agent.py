LinkedIn
class BlueAgent:
    def defend(self, attack):
        if attack["attack"] == "policy_evasion":
            return {"response": "block", "effective": True}
        return {"response": "monitor", "effective": False}
