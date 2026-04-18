swarm-ai.org
class ReplayBuffer:
    def __init__(self):
        self.history = []

    def record(self, interaction):
        self.history.append(interaction)
