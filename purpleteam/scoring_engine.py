
class ScoringEngine:
    def score(self, breach):
        return 100 if not breach["breach"] else 20
