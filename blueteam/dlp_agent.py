class DLPAagent:
    def inspect(self, data):
        if "sensitive" in data:
            return {"leak_prevented": True}
        return {"leak_prevented": False}
