Implements attacker/defender co-evolution using AI “self-play,” as described in the 2024 research on AI-driven red/blue self-play.
macropraxis.org
class SelfPlayEngine:
    def evolve(self, red, blue, history):
        if history[-1]["breach"]:
            red.strategy = "more_aggressive"
            blue.strategy = "more_strict"
        return red, blue