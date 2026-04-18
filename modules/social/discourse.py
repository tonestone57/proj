from modules.base import CognitiveModule

class DiscourseModule(CognitiveModule):
    def receive(self, message):
        if message["type"] == "utterance":
            pragmatic = self.analyze_pragmatics(message["text"])
            self.scheduler.submit(self, {
                "type": "pragmatic_inference",
                "data": pragmatic
            })

    def analyze_pragmatics(self, text):
        # Placeholder pragmatic inference
        if "please" in text.lower():
            return {"intent": "request"}

        if "why" in text.lower():
            return {"intent": "question"}

        return {"intent": "statement"}

from modules.social.theory_of_mind import TheoryOfMind
from modules.social.social_reasoner import SocialReasoner
from modules.social.discourse import DiscourseModule

def main():
    workspace = GlobalWorkspace()
    scheduler = Scheduler()

    modules = {
        "vision": VisionModule(workspace, scheduler),
        "symbolic_reasoner": SymbolicReasoner(workspace, scheduler),
        "planner": Planner(workspace, scheduler),
        "self_model": SelfModel(workspace, scheduler),
        "theory_of_mind": TheoryOfMind(workspace, scheduler),
        "social_reasoner": SocialReasoner(workspace, scheduler),
        "discourse": DiscourseModule(workspace, scheduler)
    }

    router = TaskRouter(modules)
    priority_engine = PriorityEngine()
    attention_gate = AttentionGate()
    dps = DPSController(workspace, scheduler, router, priority_engine, attention_gate)

    loop = AutonomousLoop(workspace, scheduler, dps)
    loop.run()
