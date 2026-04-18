Github
class HumanInterface:
    def present(self, action):
        return f"Action requires approval: {action}"

    def get_decision(self):
        # Placeholder for UI integration
        return "approve"
