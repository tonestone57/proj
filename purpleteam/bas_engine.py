class BASEngine:
    def simulate(self, attack, defense):
        if attack["success"] and not defense["effective"]:
            return {"breach": True}
        return {"breach": False}
