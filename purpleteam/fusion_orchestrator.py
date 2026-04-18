lasso.security
class FusionOrchestrator:
    def cycle(self, red, blue, state):
        attack = red.attack(state)
        defense = blue.defend(attack)
        return {"attack": attack, "defense": defense}
