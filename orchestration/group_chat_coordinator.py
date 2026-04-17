Implements group-chat orchestration (multi-agent collaborative reasoning).
Microsoft Developer Blogs
class GroupChatCoordinator:
    def __init__(self, agents):
        self.agents = agents
        self.turn = 0

    def step(self, message):
        agent = self.agents[self.turn % len(self.agents)]
        self.turn += 1
        return agent.respond(message)