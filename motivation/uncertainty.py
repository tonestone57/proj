import math

class UncertaintyModule:
    def compute_uncertainty(self, state):
        # SGI 2026: Quantify system uncertainty
        # Derived from property variance or entropy
        if not isinstance(state, dict): return 0.5

        history = state.get("history", [])
        if not history: return 1.0

        # Simple frequency-based uncertainty
        types = [m.get("type") for m in history]
        unique_types = set(types)

        if not unique_types: return 1.0

        # Uncertainty decreases as we see more variety (or increases with chaos)
        return len(unique_types) / len(types) if types else 1.0
