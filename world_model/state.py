import json

class WorldState:
    def __init__(self):
        self.checkpoints = {}
        self.internal_state = {
            "cognitive_load": 0,
            "active_goals": [],
            "last_action": None
        }
        self.external_state = {
            "entities": {},
            "environment_vars": {},
            "user_context": {}
        }

    def update_internal(self, key, value):
        self.internal_state[key] = value

    def update_external(self, category, key, value):
        if category in self.external_state:
            self.external_state[category][key] = value

    def snapshot(self):
        return {
            "internal": self.internal_state.copy(),
            "external": self.external_state.copy()
        }

    def track_reality_gap(self, prediction, observation):
        """
        Identifies discrepancies between predicted and observed states.
        """
        print("[WorldState] Identifying reality gaps...")
        gap = {}
        for key in observation:
            if key not in prediction:
                gap[key] = "Unexpected observation"
            elif prediction[key] != observation[key]:
                gap[key] = f"Discrepancy: predicted {prediction[key]}, observed {observation[key]}"
        return gap

    def serialize_state(self):
        """
        Serializes current state to JSON string for persistence.
        """
        print("[WorldState] Serializing state for persistence...")
        return json.dumps(self.snapshot())

    def deserialize_state(self, state_json):
        """
        Restores state from JSON string.
        """
        print("[WorldState] Restoring state from persistence...")
        data = json.loads(state_json)
        self.internal_state = data.get("internal", {})
        self.external_state = data.get("external", {})

    def checkpoint_state(self, checkpoint_id):
        """
        Saves a snapshot of the current state with a given ID.
        """
        print(f"[WorldState] Saving checkpoint: {checkpoint_id}")
        self.checkpoints[checkpoint_id] = self.snapshot()

    def rewind_to_checkpoint(self, checkpoint_id):
        """
        Restores state from a saved checkpoint.
        """
        if checkpoint_id in self.checkpoints:
            print(f"[WorldState] Rewinding to checkpoint: {checkpoint_id}")
            data = self.checkpoints[checkpoint_id]
            self.internal_state = data["internal"].copy()
            self.external_state = data["external"].copy()
        else:
            print(f"[WorldState] Error: Checkpoint {checkpoint_id} not found.")

class VMStateDigitalTwin:
    """
    Simulates a persistent Digital Twin (Firecracker microVM) state tracking.
    Supports speculative execution branching and side-effect monitoring.
    """
    def __init__(self, vm_id):
        self.vm_id = vm_id
        self.status = "stopped"
        self.resources = {"cpu": 0, "mem": 0}
        self.side_effects = []
        self.branches = {}

    def start(self):
        print(f"[VMDigitalTwin:{self.vm_id}] Starting microVM...")
        self.status = "running"

    def branch(self, branch_id):
        """
        Simulates branching the VM state for speculative execution.
        """
        print(f"[VMDigitalTwin:{self.vm_id}] Branching state to {branch_id}")
        self.branches[branch_id] = {
            "status": self.status,
            "resources": self.resources.copy(),
            "side_effects": self.side_effects[:]
        }

    def observe(self, effect):
        print(f"[VMDigitalTwin:{self.vm_id}] Observing side effect: {effect}")
        self.side_effects.append(effect)
