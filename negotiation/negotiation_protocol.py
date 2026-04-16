Implements the Progressive Negotiation Protocol (PNP).
class NegotiationProtocol:
    def __init__(self, utility_system, concession_strategy, consensus_engine):
        self.utility = utility_system
        self.concession = concession_strategy
        self.consensus = consensus_engine

    def negotiate(self, agents, proposals, rounds=5):
        for _ in range(rounds):
            best = self.consensus.consensus(agents, proposals)
            proposals = [self.concession.concede(p) for p in proposals]
        return best