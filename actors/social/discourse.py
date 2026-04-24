import ray
from core.base import CognitiveModule

@ray.remote
class DiscourseModule(CognitiveModule):
    def receive(self, message):
        if super().receive(message): return
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "utterance":
            pragmatic = self.analyze_pragmatics(message["text"])
            self.send_result("pragmatic_inference", pragmatic)

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