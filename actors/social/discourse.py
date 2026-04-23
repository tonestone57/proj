from core.base import CognitiveModule

class DiscourseModule(CognitiveModule):
    def receive(self, message):
        if message["type"] == "utterance":
            pragmatic = self.analyze_pragmatics(message["text"])
            self.scheduler.submit(self, {
                "type": "pragmatic_inference",
                "data": pragmatic
            })

    def analyze_pragmatics(self, text):
        # SGI 2026: Pragmatic analysis for intent and tone
        t_lower = str(text).lower()

        # Intent detection
        intent = "statement"
        if "?" in t_lower or any(w in t_lower for w in ["why", "how", "what", "where"]):
            intent = "question"
        elif any(w in t_lower for w in ["please", "could you", "can you"]):
            intent = "request"
        elif any(w in t_lower for w in ["must", "stop", "halt"]):
            intent = "command"

        # Tone/Affective tagging
        tone = "neutral"
        if any(w in t_lower for w in ["thanks", "good", "great", "happy"]):
            tone = "positive"
        elif any(w in t_lower for w in ["wrong", "bad", "error", "fail"]):
            tone = "negative"

        return {
            "intent": intent,
            "tone": tone,
            "complexity": len(t_lower.split())
        }

from actors.social.theory_of_mind import TheoryOfMind
from actors.social.social_reasoner import SocialReasoner
from actors.social.discourse import DiscourseModule

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
