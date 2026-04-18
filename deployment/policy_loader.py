class PolicyLoader:
    def __init__(self):
        self.policies = {}

    def load(self, name, policy):
        self.policies[name] = policy

    def get(self, name):
        return self.policies.get(name)
