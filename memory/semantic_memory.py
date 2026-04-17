class SemanticMemory:
    def __init__(self):
        self.knowledge = {}

    def store_fact(self, key, value):
        self.knowledge[key] = value

    def query(self, key):
        return self.knowledge.get(key)

3. Cognitive Modules
Each module follows the same interface:
class CognitiveModule:
    def __init__(self, workspace, scheduler):
        self.workspace = workspace
        self.scheduler = scheduler
        workspace.register(self)

    def receive(self, message):
        raise NotImplementedError