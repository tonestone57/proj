class PerformanceTracker:
    def __init__(self):
        self.history = []
        self.module_scores = {}

    def record(self, module_name, score):
        self.history.append(score)
        if module_name not in self.module_scores:
            self.module_scores[module_name] = []
        self.module_scores[module_name].append(score)

    def recent_average(self, module_name, n=10):
        scores = self.module_scores.get(module_name, [])
        if len(scores) == 0:
            return 0
        return sum(scores[-n:]) / min(len(scores), n)
