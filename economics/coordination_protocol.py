class CoordinationProtocol:
    def consensus(self, proposals):
        return sum(proposals) / len(proposals)
