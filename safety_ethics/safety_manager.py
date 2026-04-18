from safety_ethics.risk_classifier import RiskClassifier
from safety_ethics.oversight_agent import OversightAgent
from safety_ethics.governance_graph import GovernanceGraph
from safety_ethics.interpretability_monitor import InterpretabilityMonitor
from safety_ethics.deception_detector import DeceptionDetector
from safety_ethics.constraint_enforcer import ConstraintEnforcer
from safety_ethics.shutdown_controller import ShutdownController

class SafetyManager:
    def __init__(self):
        self.risk = RiskClassifier()
        self.oversight = OversightAgent(self.risk)
        self.gov = GovernanceGraph()
        self.interp = InterpretabilityMonitor()
        self.deception = DeceptionDetector()
        self.constraints = ConstraintEnforcer()
        self.shutdown = ShutdownController()

    def evaluate(self, action, internal_state):
        if not self.shutdown.is_active():
            return {"approved": False, "reason": "system shutdown"}

        if self.deception.detect(action, internal_state):
            return {"approved": False, "reason": "deception detected"}

        if not self.constraints.enforce(action):
            return {"approved": False, "reason": "constraint violation"}

        if not self.gov.enforce(action):
            return {"approved": False, "reason": "governance rule violation"}

        oversight = self.oversight.review(action)
        if not oversight["approved"]:
            return {"approved": False, "reason": f"risk: {oversight['risk']}"}

        return {"approved": True, "reason": "safe"}
