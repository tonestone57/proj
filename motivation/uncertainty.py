Measures how uncertain the AGI is about its world-model.
class UncertaintyModule:
    def compute_uncertainty(self, world_state):
        uncertainty = 0
        for entity, data in world_state["entities"].items():
            if "confidence" in data:
                uncertainty += (1 - data["confidence"])
        return uncertainty
Uncertainty = lack of confidence in world knowledge.