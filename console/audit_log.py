
class AuditLog:
    def __init__(self):
        self.entries = []

    def record(self, entry):
        self.entries.append(entry)

    def view(self):
        return self.entries
