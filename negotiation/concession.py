class ConcessionStrategy:
    def concede(self, proposal, factor=0.1):
        new_util = {k: v * (1 - factor) for k, v in proposal.utility.items()}
        return Proposal(proposal.content, new_util, proposal.agent_id)
