from negotiation.proposal import Proposal
from negotiation.utility import UtilitySystem
from negotiation.concession import ConcessionStrategy
from negotiation.consensus_engine import ConsensusEngine
from negotiation.negotiation_protocol import NegotiationProtocol
from negotiation.treaty_graph import TreatyGraph
from negotiation.compliance_engine import ComplianceEngine

class NegotiationManager:
    def __init__(self, role_weights):
        self.utility = UtilitySystem()
        self.concession = ConcessionStrategy()
        self.consensus = ConsensusEngine(role_weights)
        self.protocol = NegotiationProtocol(self.utility, self.concession, self.consensus)
        self.treaties = TreatyGraph()
        self.compliance = ComplianceEngine()

    def negotiate(self, agents, proposals):
        return self.protocol.negotiate(agents, proposals)

    def form_treaty(self, treaty):
        self.treaties.add_treaty(treaty)

Cognition (reasoning, planning, world-modeling)
Emotion (generation, appraisal, regulation)
