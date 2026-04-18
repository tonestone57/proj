class CognitiveModule:
    def __init__(self, workspace, scheduler):
        self.workspace = workspace
        self.scheduler = scheduler
        workspace.register(self)

    def receive(self, message):
        raise NotImplementedError
