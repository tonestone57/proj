class NoveltyModule:
    def __init__(self):
        self.known_patterns = set()

    def compute_novelty(self, state):
        # SGI 2026: Signal novelty drive
        state_key = str(state.get("last_action", "none"))

        if state_key in self.known_patterns:
            return 0.1

        self.known_patterns.add(state_key)
        return 0.9
