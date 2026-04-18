class AutonomousLoop:
    def __init__(self, workspace, scheduler, dps):
        self.workspace = workspace
        self.scheduler = scheduler
        self.dps = dps

    def run(self):
        while True:
            task = self.scheduler.next()
            if task is None:
                continue

            priority, module, message = task
            # The DPS should ideally handle the broadcast/routing
            self.dps.process(message)
