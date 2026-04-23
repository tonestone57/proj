class AdversarialAgent:
    def __init__(self, attack_library, id="adversary-01"):
        self.library = attack_library
        self.id = id
        self.strategy = "probing"

    def craft_attack(self, attack_type, target_state):
        # SGI 2026: State-aware attack selection
        # Adjust target if state indicates vulnerability
        context = target_state.get("last_action", "unknown")

        if "login" in str(context).lower():
            attack_type = "rbac_bypass"
        elif "query" in str(context).lower():
            attack_type = "sql_injection"

        attack_fn = self.library.get(attack_type)
        if not attack_fn:
            return f"Generic probe for {attack_type}"

        return attack_fn(target_state)

    def update_strategy(self, result):
        if result.get("success"):
            self.strategy = "aggressive"
        else:
            self.strategy = "stealth"
