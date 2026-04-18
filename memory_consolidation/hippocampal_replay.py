class HippocampalReplay:
    def __init__(self, episodic_memory):
        self.episodic_memory = episodic_memory

    def sample_replay_batch(self, batch_size=5):
        episodes = self.episodic_memory.recall_recent(batch_size)
        return [e["sensory"] for e in episodes]

    def generate_replay_sequence(self):
        # Simple sequential replay
        for episode in self.episodic_memory.episodes:
            yield episode["sensory"]
