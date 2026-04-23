class Proposal:
    def __init__(self, content, utility, agent_id):
        self.content = content
        self.utility = utility # Dict mapping agent_id -> utility value
        self.agent_id = agent_id

class ProposalEngine:
    def generate(self, agent, context):
        # SGI 2026: Reasoning-aware proposal generation
        context_str = str(context).lower()

        # Adaptive utility based on context
        utilities = {agent: 0.9}
        base_utility = 0.4

        if "resource" in context_str:
            base_utility = 0.6
        elif "security" in context_str:
            base_utility = 0.8 # Security is high stakes for everyone

        # Add entry for other known agents in a real scenario
        # Here we just represent others as a group
        utilities["others"] = base_utility

        return Proposal(f"Strategic Proposal from {agent} on {context}", utilities, agent)
