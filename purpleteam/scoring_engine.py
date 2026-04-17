Implements scoring of detection coverage, time-to-detect, and time-to-remediate, as described in Autonomous Purple Teaming.
LinkedIn
class ScoringEngine:
    def score(self, breach):
        return 100 if not breach["breach"] else 20