class CausalGraph:
    def __init__(self):
        self.graph = {}

    def add_causal_link(self, cause, effect):
        if cause not in self.graph:
            self.graph[cause] = []
        self.graph[cause].append(effect)

    def get_effects(self, cause):
        return self.graph.get(cause, [])

    def get_causes(self, effect):
        return [c for c, effects in self.graph.items() if effect in effects]
