class ConcessionStrategy:
    def __init__(self, patience=5):
        self.patience = patience

    def concede(self, proposal, current_round=0, factor=0.05):
        # SGI 2026: Concession with variable thresholds and round-awareness
        # Concession increases as rounds progress
        concession_mult = factor * (1 + (current_round / self.patience))

        new_util = {}
        for agent, util in proposal.utility.items():
            if agent == proposal.agent_id:
                # Proposer lowers their own expected utility
                new_util[agent] = max(0.4, util - concession_mult)
            else:
                # Proposer increases offered utility to others
                new_util[agent] = min(1.0, util + (concession_mult / 2))

        return Proposal(proposal.content + f" (Round {current_round} Concession)", new_util, proposal.agent_id)
