galileo.ai
class ConfidenceMonitor:
    def evaluate(self, result):
        return result.get("confidence", 0.0)
