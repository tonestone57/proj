Tracks agent confidence and triggers escalation.
galileo.ai
class ConfidenceMonitor:
    def evaluate(self, result):
        return result.get("confidence", 0.0)