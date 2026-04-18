class ConsolidationScheduler:
    def __init__(self):
        self.priority_threshold = 0.5

    def select_for_replay(self, episodic_memory):
        selected = []
        for ep in episodic_memory.episodes:
            if ep.get("strength", 0.5) < self.priority_threshold:
                selected.append(ep)
        return selected
