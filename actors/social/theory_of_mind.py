from core.base import CognitiveModule

class TheoryOfMind(CognitiveModule):
    def __init__(self, workspace, scheduler):
        super().__init__(workspace, scheduler)
        self.agent_models = {}

    def receive(self, message):
        if message["type"] == "social_event":
            self.update_agent_model(message["agent"], message["data"])

        if message["type"] == "infer_intention":
            intention = self.infer_intention(message["agent"])
            self.scheduler.submit(self, {
                "type": "intention_inferred",
                "agent": message["agent"],
                "data": intention
            })

    def update_agent_model(self, agent, data):
        if agent not in self.agent_models:
            self.agent_models[agent] = {
                "beliefs": {},
                "goals": {},
                "emotions": {},
                "history": []
            }

        self.agent_models[agent]["history"].append(data)

        # Example: update beliefs or emotions
        if "belief" in data:
            self.agent_models[agent]["beliefs"].update(data["belief"])

        if "emotion" in data:
            self.agent_models[agent]["emotions"].update(data["emotion"])

    def infer_intention(self, agent):
        model = self.agent_models.get(agent, None)
        if not model:
            return {"intention": "unknown"}

        # Placeholder inference logic
        if "goal" in model["beliefs"]:
            return {"intention": model["beliefs"]["goal"]}

        return {"intention": "uncertain"}
