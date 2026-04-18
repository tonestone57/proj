class EpisodicMemory:
    def __init__(self):
        self.episodes = []

    def add_episode(self, data):
        self.episodes.append(data)

    def recall_recent(self, n=5):
        return self.episodes[-n:]
