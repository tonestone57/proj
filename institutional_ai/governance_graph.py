class GovernanceGraph:
    def __init__(self):
        self.nodes = {} # agent -> role
        self.rules = [] # list of (source_role, target_role, predicate)

    def add_node(self, name, role):
        self.nodes[name] = role

    def add_governance_rule(self, source_role, target_role, predicate):
        self.rules.append((source_role, target_role, predicate))

    def enforce(self, action):
        # SGI 2026: Role-based governance enforcement
        agent = action.get("agent_id", "unknown")
        agent_role = self.nodes.get(agent, "guest")

        target = action.get("target_id")
        target_role = self.nodes.get(target, "resource")

        for s_role, t_role, predicate in self.rules:
            if s_role == agent_role and t_role == target_role:
                if not predicate(action):
                    return False
        return True
