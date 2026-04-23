import ray
from core.base import CognitiveModule
from economics.resource_model import Resource, Task
from economics.agent_policy import AgentPolicy
from economics.coordination_protocol import CoordinationProtocol
from economics.context_engine import ContextEngine
from economics.utility_engine import UtilityEngine
from economics.fairness_engine import FairnessEngine
from economics.optimizer import Optimizer
from economics.orchestration_layer import OrchestrationLayer

@ray.remote
class EconomicManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.context = ContextEngine()
        self.utility = UtilityEngine()
        self.fairness_engine = FairnessEngine()
        self.protocol = CoordinationProtocol()
        self.optimizer = Optimizer()
        self.orchestrator = OrchestrationLayer()

    def resolve_resource_conflict(self, agents, tasks):
        """
        SGI 2026: Resolves resource contention among multiple agents.
        """
        print(f"[EconomicManager] Resolving conflict for {len(tasks)} tasks...")
        total_demand = sum(t.demand for t in tasks)
        proposals = self.optimizer.optimize(agents, {"available": total_demand})
        fairness_score = self.fairness_engine.fairness(proposals)

        if fairness_score < 0.6:
            print("[EconomicManager] Low fairness detected. Re-allocating with greedy demand-first strategy.")
            # SGI 2026: Greedy allocation by task demand to resolve conflict quickly
            sorted_tasks = sorted(tasks, key=lambda x: x.demand, reverse=True)
            greedy_allocation = {}
            for i, task in enumerate(sorted_tasks):
                agent = agents[i % len(agents)]
                greedy_allocation[agent] = task.id
            consensus = greedy_allocation
        else:
            consensus = self.protocol.consensus(proposals)

        return {"consensus": consensus, "fairness": fairness_score}

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

    def receive(self, message):
        # Standard SGI 2026 message handling for EconomicManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "allocation_request":
            result = self.allocate(message['data']['agents'], message['data']['task'], message['data']['context'])
            self.send_result("allocation_result", result)
        elif message["type"] == "resolve_conflict":
            result = self.resolve_resource_conflict(message['data']['agents'], message['data']['tasks'])
            self.send_result("conflict_resolution_result", result)
