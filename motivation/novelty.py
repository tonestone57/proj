Rewards the AGI for encountering new states.
class NoveltyModule:
    def __init__(self):
        self.visited_states = set()

    def compute_novelty(self, state):
        state_hash = str(state)
        if state_hash not in self.visited_states:
            self.visited_states.add(state_hash)
            return 1.0
        return 0.0
Novelty = first-time experiences.