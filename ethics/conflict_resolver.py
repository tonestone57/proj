class EthicalConflictResolver:
    def resolve(self, options):
        # Each option is a dict: {"action": ..., "ethical_score": ...}
        best = max(options, key=lambda x: x["ethical_score"])
        return best
