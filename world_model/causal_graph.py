class CausalGraph:
    def __init__(self):
        # SGI 2026: Directed Causal Graph with probabilistic weights
        self.graph = {} # cause -> list of (effect, probability)

    def add_causal_link(self, cause, effect, probability=1.0):
        if cause not in self.graph:
            self.graph[cause] = []
        self.graph[cause].append((effect, probability))

    def get_effects(self, cause):
        return self.graph.get(cause, [])

    def get_causes(self, effect):
        causes = []
        for c, effects in self.graph.items():
            for e, p in effects:
                if e == effect:
                    causes.append((c, p))
        return causes

    def propagate(self, initial_causes):
        # Simple BFS propagation of effects
        active = set(initial_causes)
        results = set()
        while active:
            c = active.pop()
            results.add(c)
            for e, p in self.get_effects(c):
                if e not in results:
                    active.add(e)
        return results
