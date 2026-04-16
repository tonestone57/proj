Inspired by Barry & Love (2023):
Replay is selective, prioritizing weakly learned or high-value memories. Oxford Academic
class ConsolidationScheduler:
    def __init__(self):
        self.priority_threshold = 0.5

    def select_for_replay(self, episodic_memory):
        selected = []
        for ep in episodic_memory.episodes:
            if ep.get("strength", 0.5) < self.priority_threshold:
                selected.append(ep)
        return selected
This implements active, reinforcement-guided replay.