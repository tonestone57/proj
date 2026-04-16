Implements traceability and accountability as required by HITL frameworks.
Permit.io
class AuditLog:
    def __init__(self):
        self.entries = []

    def record(self, entry):
        self.entries.append(entry)

    def view(self):
        return self.entries