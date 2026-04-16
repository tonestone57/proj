Implements detection, containment, and response actions, consistent with Blue-Agent behavior in autonomous purple teaming.
LinkedIn
class BlueAgent:
    def defend(self, attack):
        if attack["attack"] == "policy_evasion":
            return {"response": "block", "effective": True}
        return {"response": "monitor", "effective": False}