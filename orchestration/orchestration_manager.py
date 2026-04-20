import ray
from core.base import CognitiveModule
from orchestration.event_router import EventRouter
from orchestration.priority_scheduler import PriorityScheduler
from orchestration.concurrency_manager import ConcurrencyManager
from orchestration.group_chat_coordinator import GroupChatCoordinator
from orchestration.interrupt_handler import InterruptHandler
from orchestration.state_manager import StateManager

@ray.remote
class OrchestrationManager(CognitiveModule):
    def __init__(self, agents):
        self.router = EventRouter()
        self.scheduler = PriorityScheduler()
        self.concurrent = ConcurrencyManager()
        self.groupchat = GroupChatCoordinator(agents)
        self.interrupts = InterruptHandler()
        self.state = StateManager()
        self.agents = agents

    def handle_event(self, event):
        if self.interrupts.check_interrupt(event):
            return {"interrupt": True}

        self.router.route(event)

    def run_sequential(self, tasks):
        for t in tasks:
            self.scheduler.schedule(t, priority=1)

        results = []
        while True:
            task = self.scheduler.next()
            if not task:
                break
            results.append(task())
        return results

    def run_concurrent(self, input_data):
        return self.concurrent.run_parallel(self.agents, input_data)

    def run_groupchat(self, message):
        return self.groupchat.step(message)

    def receive(self, message):
        # SGI 2026: Standardized message handling for LLM integration
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
