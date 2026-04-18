import ray
import time
import asyncio

# Import existing module logic for reuse
from actors.reasoner_actor import ReasonerActor as ReasonerLogic
from actors.coding_actor import CodingActor as CodingLogic

# Ray Initialization
ray.init(ignore_reinit_error=True)

# Mock classes to allow existing modules to initialize without side effects
class MockWorkspace:
    def register(self, module): pass
class MockScheduler:
    def submit(self, module, message, priority=1.0): pass

@ray.remote
class CodingActor:
    def __init__(self):
        # Reuse existing logic but bypass old sync infrastructure
        self.logic = CodingLogic(MockWorkspace(), MockScheduler())

    def execute(self, code):
        print(f"[CodingActor] Executing code...")
        return self.logic.execute_code(code)

@ray.remote
class ReasonerActor:
    def __init__(self):
        self.logic = ReasonerLogic(MockWorkspace(), MockScheduler())

    def reason(self, query):
        print(f"[ReasonerActor] Reasoning about: {query}")
        return self.logic.reason(query)

@ray.remote
class IntegratorHub:
    def __init__(self):
        self.state = {"focus": "idle", "history": []}

    def integrate(self, results):
        for res in results:
            print(f"[Hub] Integrating result: {res}")
            self.state["history"].append(res)
        return self.state

    def get_focus(self):
        return "Solve math and optimize code"

class DriveEngine:
    def needs_proactive_effort(self, state):
        # Simple entropy-like trigger: if history is short, we need more "knowledge"
        return len(state.get("history", [])) < 5

async def cognitive_cycle():
    hub = IntegratorHub.remote()
    coder = CodingActor.remote()
    reasoner = ReasonerActor.remote()
    drives = DriveEngine()

    pending_futures = []

    print("Ray-based APW SGI System Initialized.")
    print("Architecture: Asynchronous Predictive Workspace")

    # The Heartbeat Loop
    for tick in range(10):
        print(f"\n--- Heartbeat Tick {tick+1} ---")

        # 1. Integrate: Hub updates the "Global Workspace" state
        if pending_futures:
            # Check which tasks are done
            done, pending_futures = ray.wait(pending_futures, timeout=0)
            if done:
                results = ray.get(done)
                await hub.integrate.remote(results)

        global_state = await hub.integrate.remote([]) # Just to get latest state

        # 2. Drive: Does the internal state require action?
        if drives.needs_proactive_effort(global_state):
            print("[Drives] High Entropy detected. Triggering proactive tasks.")
            # 3. Broadcast: Tell all modules what the current "Top Priority" is
            # In Ray, we trigger the actors asynchronously
            if tick % 2 == 0:
                future = reasoner.reason.remote("math.factorial(6)")
            else:
                future = coder.execute.remote("print('Proactive self-test')")
            pending_futures.append(future)

        await asyncio.sleep(0.5)

    print("\nAPW Demo complete.")

if __name__ == "__main__":
    asyncio.run(cognitive_cycle())
