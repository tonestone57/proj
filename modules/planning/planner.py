from modules.base import CognitiveModule

class Planner(CognitiveModule):
    def receive(self, message):
        if message["type"] == "goal":
            plan = self.create_plan(message["data"])
            self.scheduler.submit(self, {"type": "plan", "data": plan})

    def create_plan(self, goal):
        return ["step1", "step2", "step3"]