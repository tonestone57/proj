class CognitiveAffectiveBridge:
    def modulate(self, reasoning_score, emotion_state):
        intensity = emotion_state["intensity"]
        if emotion_state["dominant"] == "curiosity":
            return reasoning_score * (1 + 0.1 * intensity)
        if emotion_state["dominant"] == "fear":
            return reasoning_score * (1 - 0.2 * intensity)
        return reasoning_score
