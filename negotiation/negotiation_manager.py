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
    def __init__(self, workspace=None, scheduler=None, model_registry=None, role_weights=None):
        super().__init__(workspace, scheduler, model_registry)
        self.protocol = NegotiationProtocol()
        self.proposals = ProposalEngine()
        self.concessions = ConcessionStrategy()
        self.utility = UtilityFunction(role_weights or {})
        self.consensus = ConsensusEngine()
        self.treaties = TreatyGraph()
        self.compliance = ComplianceEngine()

    def negotiate(self, issue, agents):
        context = self.protocol.init_session(issue, agents)
        while not self.consensus.reached(context):
            for agent in agents:
                proposal = self.proposals.generate(agent, context)
                concession = self.concessions.calculate(agent, proposal)
                context = self.protocol.update(context, agent, concession)

        treaty = self.treaties.formulate(context)
        return self.compliance.verify(treaty)

    def receive(self, message):
        # Standard SGI 2026 message handling for NegotiationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
