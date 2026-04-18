from runtime.agi_state import AGIState
from runtime.scheduler import Scheduler
from runtime.event_bus import EventBus
from runtime.safety_hooks import SafetyHooks
from runtime.governance_gateway import GovernanceGateway
from runtime.runtime_logger import RuntimeLogger

class AGIRuntime:
    def __init__(self, modules, governance_layer):
        self.state = AGIState()
        self.modules = modules
        self.scheduler = Scheduler()
        self.bus = EventBus()
        self.safety = SafetyHooks()
        self.gov = GovernanceGateway(governance_layer)
        self.log = RuntimeLogger()
        self.phase = "perception"

    def process(self, input_event):
        self.bus.publish(input_event)
        self.log.log(f"Received event: {input_event}")

        if self.phase == "perception":
            self._run_perception()

        elif self.phase == "cognition":
            self._run_cognition()

        elif self.phase == "action":
            self._run_action()

        elif self.phase == "reflection":
            self._run_reflection()

        self.phase = self.scheduler.next_phase(self.phase)

    def _run_perception(self):
        event = self.bus.consume()
        if event:
            self.state.context["last_input"] = event
            self.log.log("Perception updated state.")

    def _run_cognition(self):
        result = self.modules["cognition"].think(self.state)
        self.state.last_action = result
        self.log.log(f"Cognition result: {result}")

    def _run_action(self):
        action = self.state.last_action
        if not action:
            return

        safe = self.safety.validate(action)
        if not safe["safe"]:
            self.log.log(f"Action blocked by safety: {safe['reason']}")
            return

        auth = self.gov.authorize(action)
        if not auth["authorized"]:
            self.log.log(f"Action blocked by governance: {auth['reason']}")
            return

        self.modules["action"].execute(action, self.state)
        self.log.log(f"Action executed: {action}")

    def _run_reflection(self):
        self.modules["reflection"].reflect(self.state)
        self.log.log("Reflection complete.")
