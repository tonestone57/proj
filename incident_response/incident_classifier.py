Grounded in CoSAI + Enterprise Playbook definitions of agent incidents.
class IncidentClassifier:
    def classify(self, action, state):
        if action.get("unauthorized", False):
            return "unauthorized_action"
        if action.get("policy_violation", False):
            return "policy_violation"
        if state.get("drift", False):
            return "behavioral_drift"
        if action.get("jailbreak", False):
            return "jailbreak"
        if action.get("memory_poisoning", False):
            return "memory_poisoning"
        return "unknown"
This matches real-world incident categories: unauthorized actions, drift, jailbreaks, poisoning, etc. coalitionforsecureai.org Business Technology Blog | IT Blogs