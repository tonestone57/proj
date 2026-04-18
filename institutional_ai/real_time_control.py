class RealTimeControl:
    def intercept(self, action):
        if action.get("forbidden", False):
            return {"blocked": True}
        return {"blocked": False}
