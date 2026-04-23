import time

class PerformanceTracker:
    def __init__(self):
        self.history = [] # List of (timestamp, overall_score)
        self.module_scores = {} # module_name -> list of (timestamp, score)

    def record(self, module_name, score):
        ts = time.time()
        self.history.append((ts, score))
        if module_name not in self.module_scores:
            self.module_scores[module_name] = []
        self.module_scores[module_name].append((ts, score))

    def analyze(self, module_name=None):
        # SGI 2026: Analyze performance trends
        target = self.module_scores.get(module_name, []) if module_name else self.history

        if not target: return {"status": "no_data"}

        scores = [s[1] for s in target]
        avg = sum(scores) / len(scores)

        # Simple trend analysis: compare first half to second half
        mid = len(scores) // 2
        trend = "stable"
        if mid > 0:
            first_half = sum(scores[:mid]) / mid
            second_half = sum(scores[mid:]) / (len(scores) - mid)
            if second_half > first_half * 1.05: trend = "improving"
            elif second_half < first_half * 0.95: trend = "declining"

        return {
            "average_score": avg,
            "data_points": len(scores),
            "trend": trend,
            "last_score": scores[-1]
        }
