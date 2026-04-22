
class SelfPlayEngine:
    def evolve(self, red, blue, history):
        if history[-1]["breach"]:
            red.strategy = "more_aggressive"
            blue.strategy = "more_strict"
        return red, blue
