import ray
import time

ray.init()

# Define the Spoke as a Ray Actor
@ray.remote
class CodingActor:
    def write_tests(self, code):
        # Heavy CPU work happens here, completely bypassing the GIL
        return "Tests completed."

# Define the Hub
@ray.remote
class IntegratorHub:
    def __init__(self):
        self.state = "Idle"

    def process_result(self, result):
        print(f"Hub updating state with: {result}")

def main():
    # Initialization
    hub = IntegratorHub.remote()
    coder = CodingActor.remote()

    print("Ray-based APW SGI System Initialized.")

    # The Heartbeat / Autonomous Loop
    # We'll run this for a few iterations for demonstration
    for _ in range(10):
        # Trigger the actor asynchronously (returns a future)
        future = coder.write_tests.remote("def foo(): pass")

        # Hub processes it when ready, without blocking the main loop
        hub.process_result.remote(future)

        print("Heartbeat tick...")
        time.sleep(0.1)

    print("Demo complete.")

if __name__ == "__main__":
    main()
