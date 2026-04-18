from economics.resource_model import Resource, Task
from economics.agent_policy import AgentPolicy
from economics.coordination_protocol import CoordinationProtocol
from economics.context_engine import ContextEngine
from economics.utility_engine import UtilityEngine
from economics.fairness_engine import FairnessEngine
from economics.optimizer import Optimizer
from economics.orchestration_layer import OrchestrationLayer

class EconomicManager:
    def __init__(self):
        self.context = ContextEngine()
        self.utility = UtilityEngine()
        self.fairness_engine = FairnessEngine()
        self.protocol = CoordinationProtocol()
        self.optimizer = Optimizer()
        self.orchestrator = OrchestrationLayer()

    def allocate(self, agents, task, context):
        adjusted_demand = self.context.adjust(task.demand, context)
        proposals = self.optimizer.optimize(agents, {"available": adjusted_demand})
        consensus = self.protocol.consensus(proposals)
        utilities = [self.utility.compute(p, adjusted_demand) for p in proposals]
        fairness = self.fairness_engine.fairness(proposals)
        return {
            "proposals": proposals,
            "consensus_allocation": consensus,
            "utilities": utilities,
            "fairness": fairness
        }
