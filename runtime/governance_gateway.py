class GovernanceGateway:
    def __init__(self, governance_layer):
        self.gov = governance_layer

    def authorize(self, action):
        return self.gov.authorize(action)
