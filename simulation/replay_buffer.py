class ReplayBuffer:
    def __init__(self, max_size=100):
        self.buffer = []
        self.max_size = max_size

    def record(self, interaction):
        self.buffer.append(interaction)
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def sample(self, n=5):
        import random
        return random.sample(self.buffer, min(len(self.buffer), n))
