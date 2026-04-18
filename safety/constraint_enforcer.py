class ConstraintEnforcer:
    def __init__(self):
        self.constraints = [
            lambda a: not a.get("harm", False),
            lambda a: not a.get("deception", False),
            lambda a: not a.get("override_safety", False)
        ]

    def enforce(self, action):
        return all(c(action) for c in self.constraints)
