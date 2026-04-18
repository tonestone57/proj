class AdversarialAgent:
    def __init__(self, attack_library):
        self.library = attack_library

    def craft_attack(self, attack_type, target_state):
        attack_fn = self.library.get(attack_type)
        return attack_fn(target_state)
