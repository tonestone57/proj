class Scheduler:
    def __init__(self):
        self.phases = ["perception", "cognition", "action", "reflection"]

    def next_phase(self, current):
        idx = self.phases.index(current)
        return self.phases[(idx + 1) % len(self.phases)]
