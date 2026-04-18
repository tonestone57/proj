class SemanticMemory:
    def __init__(self):
        self.knowledge = {}

    def store_fact(self, key, value):
        self.knowledge[key] = value

    def query(self, key):
        return self.knowledge.get(key)

class CognitiveModule:
    def __init__(self, workspace, scheduler):
        self.workspace = workspace
        self.scheduler = scheduler
        workspace.register(self)

    def receive(self, message):
        raise NotImplementedError
