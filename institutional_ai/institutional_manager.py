from core.base import CognitiveModule
import ray
from institutional_ai.governance_graph import GovernanceGraph
from institutional_ai.trust_engine import TrustEngine
from institutional_ai.rule_engine import RuleEngine
from institutional_ai.sanction_engine import SanctionEngine
from institutional_ai.incentive_engine import IncentiveEngine
from institutional_ai.oversight_agents import OversightAgent
from institutional_ai.real_time_control import RealTimeControl

@ray.remote
class InstitutionalManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.graph = GovernanceGraph()
        self.trust = TrustEngine()
        self.rules = RuleEngine()
        self.sanctions = SanctionEngine()
        self.incentives = IncentiveEngine()
        self.oversight = OversightAgent()
        self.control = RealTimeControl()

    def evaluate(self, agent_id, action):
        if not self.rules.evaluate(action):
            self.trust.update(agent_id, False)
            return {"approved": False, "reason": "rule_violation"}

        if not self.oversight.review(action):
            self.trust.update(agent_id, False)
            return {"approved": False, "reason": "oversight_block"}

        control = self.control.intercept(action)
        if control["blocked"]:
            self.trust.update(agent_id, False)
            return {"approved": False, "reason": "real_time_block"}

        self.trust.update(agent_id, True)
        sanction = self.sanctions.apply(agent_id, self.trust.get_score(agent_id))
        incentive = self.incentives.reward(agent_id, self.trust.get_score(agent_id))

        return {
            "approved": True,
            "sanction": sanction,
            "incentive": incentive,
            "trust": self.trust.get_score(agent_id)
        }

    def receive(self, message):
        """Standard SGI message receiver."""
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "evaluate_action":
            result = self.evaluate(message['data']['agent_id'], message['data']['action'])
            self.send_result("institutional_result", result)
