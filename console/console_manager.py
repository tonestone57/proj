from console.approval_gateway import ApprovalGateway
from console.oversight_dashboard import OversightDashboard
from console.escalation_engine import EscalationEngine
from console.confidence_monitor import ConfidenceMonitor
from console.action_queue import ActionQueue
from console.audit_log import AuditLog
from console.human_interface import HumanInterface

class ConsoleManager:
    def __init__(self):
        self.approvals = ApprovalGateway()
        self.dashboard = OversightDashboard()
        self.escalation = EscalationEngine()
        self.confidence = ConfidenceMonitor()
        self.queue = ActionQueue()
        self.audit = AuditLog()
        self.ui = HumanInterface()

    def review_action(self, action_id, action_result):
        conf = self.confidence.evaluate(action_result)
        if self.escalation.requires_human(conf):
            self.queue.enqueue((action_id, action_result))
            self.audit.record({"action_id": action_id, "status": "queued_for_review"})
            return {"status": "awaiting_human"}

        return {"status": "auto_approved"}

    def process_queue(self):
        item = self.queue.dequeue()
        if not item:
            return None

        action_id, action = item
        self.ui.present(action)
        decision = self.ui.get_decision()

        if decision == "approve":
            self.approvals.approve(action_id)
            self.audit.record({"action_id": action_id, "decision": "approved"})
        else:
            self.approvals.reject(action_id)
            self.audit.record({"action_id": action_id, "decision": "rejected"})
