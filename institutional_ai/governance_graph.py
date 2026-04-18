class GovernanceGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_role(self, agent_id, role):
        self.nodes[agent_id] = role

    def add_constraint(self, source, target, rule):
        self.edges.append((source, target, rule))

    def enforce(self, action):
        for source, target, rule in self.edges:
            if not rule(action):
                return False
        return True
