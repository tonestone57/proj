import time

class AutobiographicalMemory:
    def __init__(self, capacity=1000):
        self.episodes = []
        self.capacity = capacity

    def store_episode(self, data):
        # SGI 2026: Episodic storage of self-states
        entry = {
            "timestamp": time.time(),
            "data": data,
            "salience": 0.5
        }
        self.episodes.append(entry)
        if len(self.episodes) > self.capacity:
            self.episodes.pop(0)

    def recall_recent(self, n=5):
        return self.episodes[-n:]
