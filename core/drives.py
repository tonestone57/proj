import math

THRESHOLD_REPLAN = 2.0
THRESHOLD_CONSOLIDATE = 0.5

def calculate_entropy(state):
    """
    Calculates the entropy of the system state based on message history.
    Formula: S = - sum P(xi) log P(xi)
    """
    history = state.get("history", [])
    if not history:
        return 1.0  # High entropy for empty state

    # Count occurrences of different message types
    counts = {}
    for msg in history:
        msg_type = msg.get("type", "unknown") if isinstance(msg, dict) else str(type(msg))
        counts[msg_type] = counts.get(msg_type, 0) + 1

    total = len(history)
    entropy = 0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy

class DriveEngine:
    def __init__(self):
        self.entropy = 0.0

    def evaluate_state(self, state):
        self.entropy = calculate_entropy(state)
        return self.entropy

    def update_objective_priorities(self):
        # Placeholder for dynamic priority updates based on drives
        pass
