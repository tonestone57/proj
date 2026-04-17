Implements Microsoft’s checkpoint-pause-resume pattern for human approval.
Microsoft Community
class ApprovalGateway:
    def __init__(self):
        self.pending = {}

    def request_approval(self, action_id, action):
        self.pending[action_id] = {"action": action, "status": "waiting"}
        return {"requires_approval": True}

    def approve(self, action_id):
        if action_id in self.pending:
            self.pending[action_id]["status"] = "approved"
            return True
        return False

    def reject(self, action_id):
        if action_id in self.pending:
            self.pending[action_id]["status"] = "rejected"
            return True
        return False

    def status(self, action_id):
        return self.pending.get(action_id, {"status": "unknown"})