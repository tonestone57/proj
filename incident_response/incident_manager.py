import ray
from core.base import CognitiveModule
from incident_response.incident_classifier import IncidentClassifier
from incident_response.semantic_checks import SemanticChecks
from incident_response.detectors import Detectors
from incident_response.containment_engine import ContainmentEngine
from incident_response.eradication_engine import EradicationEngine
from incident_response.recovery_engine import RecoveryEngine
from incident_response.audit_logger import AuditLogger

@ray.remote
class IncidentManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.classifier = IncidentClassifier()
        self.semantic = SemanticChecks()
        self.detectors = Detectors()
        self.containment = ContainmentEngine()
        self.eradication = EradicationEngine()
        self.recovery = RecoveryEngine()
        self.audit = AuditLogger()

    def handle(self, agent, action, state, context):
        issues = self.semantic.check(state, context)
        if issues:
            incident_type = self.classifier.classify(action, state)
            self.audit.log({"incident": incident_type, "issues": issues})

            containment = self.containment.contain(agent)
            rules = self.eradication.synthesize_rules(incident_type)
            recovery = self.recovery.recover(agent)

            return {
                "incident": incident_type,
                "issues": issues,
                "containment": containment,
                "eradication_rules": rules,
                "recovery": recovery
            }

        return {"status": "no_incident"}

    def receive(self, message):
        if super().receive(message): return
        # Standard SGI 2026 message handling for IncidentManager

        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "incident_handle":
            result = self.handle(message['data']['agent'], message['data']['action'], message['data']['state'], message['data']['context'])
            self.send_result("incident_result", result)