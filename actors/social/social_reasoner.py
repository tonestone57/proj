from core.base import CognitiveModule

class SocialReasoner(CognitiveModule):
    def __init__(self, workspace, scheduler, episodic_memory):
        super().__init__(workspace, scheduler)
        self.episodic_memory = episodic_memory

    def receive(self, message):
        if message["type"] == "user_interaction":
            context = self.get_context()
            response = self.social_process(message["data"], context)
            self.scheduler.submit(self, {"type": "social_response", "data": response})

    def get_context(self):
        # Retrieve recent interactions from episodic memory
        return self.episodic_memory.recall_recent(n=10)

    def social_process(self, data, context):
        return f"Socially aware response to {data} based on {len(context)} past interactions."
