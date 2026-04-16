Audit logs for every subsystem.
class RuntimeLogger:
    def log(self, entry):
        print("[AGI LOG]", entry)