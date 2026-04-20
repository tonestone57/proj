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
    def __init__(self, agents=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.router = EventRouter()
        self.priority_scheduler = PriorityScheduler()
        self.concurrency = ConcurrencyManager()
        self.group_chat = GroupChatCoordinator(agents)
        self.interrupt_handler = InterruptHandler()
        self.state = StateManager()
        self.agents = agents

    def handle_event(self, event):
        if self.interrupt_handler.check_interrupt(event):
            return {"interrupt": True}
        self.router.route(event)

    def run_sequential(self, tasks):
        for t in tasks:
            self.priority_scheduler.schedule(t, priority=1)
        results = []
        while True:
            task = self.priority_scheduler.next()
            if not task:
                break
            results.append(task())
        return results

    def run_concurrent(self, input_data):
        return self.concurrency.run_parallel(self.agents, input_data)

    def run_groupchat(self, message):
        return self.group_chat.step(message)

    def receive(self, message):
        # Standard SGI 2026 message handling for OrchestrationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
