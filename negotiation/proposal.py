A clean structure for negotiation proposals.
class Proposal:
    def __init__(self, content, utility, agent_id):
        self.content = content
        self.utility = utility
        self.agent_id = agent_id