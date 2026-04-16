Based on DRAMA’s control-plane/worker-plane separation for dynamic task reassignment.
class OrchestrationLayer:
    def orchestrate(self, agents, tasks):
        return {agent.agent_id: tasks[i % len(tasks)].id for i, agent in enumerate(agents)}