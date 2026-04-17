Inspired by WEF’s functional classification of agents (role, autonomy, predictability, context). The World Economic Forum
class RoleDefinitions:
    def __init__(self):
        self.roles = {
            "worker": {"autonomy": "low"},
            "coordinator": {"autonomy": "medium"},
            "governor": {"autonomy": "high"},
            "auditor": {"autonomy": "restricted"}
        }

    def get_role(self, agent_id):
        return self.roles.get(agent_id, {})