import ray
from core.base import CognitiveModule
from negotiation.negotiation_protocol import NegotiationProtocol
from negotiation.proposal import ProposalEngine
from negotiation.concession import ConcessionStrategy
from negotiation.utility import UtilityFunction
from negotiation.consensus_engine import ConsensusEngine
from negotiation.treaty_graph import TreatyGraph
from negotiation.compliance_engine import ComplianceEngine

@ray.remote
class NegotiationManager(CognitiveModule):
    def __init__(self, role_weights=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        weights = role_weights or {}
        self.utility = UtilityFunction(weights)
        self.concessions = ConcessionStrategy()
        self.consensus = ConsensusEngine(weights)
        self.protocol = NegotiationProtocol(self.utility, self.concessions, self.consensus)
        self.proposals = ProposalEngine()
        self.treaties = TreatyGraph()
        self.compliance = ComplianceEngine()

    def negotiate(self, issue, agents):
        # SGI 2026: Iterative negotiation logic
        # 1. Initial proposals
        proposals = [self.proposals.generate(a, issue) for a in agents]

        # 2. Protocol handles the consensus loop and concessions
        best = self.protocol.negotiate(agents, proposals, rounds=5)

        # 3. Finalize treaty and verify compliance
        treaty = self.treaties.formulate(best)
        return self.compliance.verify(treaty)

    def receive(self, message):
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "negotiation_request":
            result = self.negotiate(message['data']['issue'], message['data']['agents'])
            self.send_result("negotiation_result", result)
