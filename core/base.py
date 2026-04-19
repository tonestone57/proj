import ray

class CognitiveModule:
    def __init__(self, workspace, scheduler):
        self.workspace = workspace
        self.scheduler = scheduler
        # In Ray, we need to register the actor handle, not 'self'
        # But we'll do this registration in the main initialization to be sure
        pass

    def receive(self, message):
        raise NotImplementedError
