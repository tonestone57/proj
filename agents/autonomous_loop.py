class AutonomousLoop:
    def __init__(self, workspace, scheduler):
        self.workspace = workspace
        self.scheduler = scheduler

    def run(self):
        while True:
            task = self.scheduler.next()
            if task is None:
                continue

            priority, module, message = task
            self.workspace.broadcast(message)