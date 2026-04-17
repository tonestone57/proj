Uses emotional state to influence decisions.
class AffectiveReasoner:
    def reason(self, affective_state, context):
        valence = affective_state["valence"]
        arousal = affective_state["arousal"]

        # Example reasoning logic
        if valence < -0.5:
            return {"strategy": "avoid", "confidence": 0.8}

        if valence > 0.5:
            return {"strategy": "approach", "confidence": 0.8}

        if arousal > 0.7:
            return {"strategy": "act_fast", "confidence": 0.6}

        return {"strategy": "neutral", "confidence": 0.5}
This is the AGI’s System-2 emotional reasoning.