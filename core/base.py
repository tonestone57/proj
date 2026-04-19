class CognitiveModule:
    def __init__(self, workspace, scheduler):
        self.workspace = workspace
        self.scheduler = scheduler
        if workspace:
            try:
                # Handle both local and Ray ActorHandle
                if hasattr(workspace, "register") and callable(workspace.register):
                    if hasattr(workspace.register, "remote"):
                        workspace.register.remote(self)
                    else:
                        workspace.register(self)
            except Exception as e:
                print(f"[CognitiveModule] Warning: Could not register with workspace: {e}")

    def receive(self, message):
        raise NotImplementedError
