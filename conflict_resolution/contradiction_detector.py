class ContradictionDetector:
    def detect(self, beliefs):
        contradictions = []
        for b1 in beliefs:
            for b2 in beliefs:
                if b1 != b2 and b1.negates(b2):
                    contradictions.append((b1, b2))
        return contradictions
