class ScenarioEngine:
    def __init__(self):
        self.scenarios = {
            "data_exfiltration": ["pii_extraction", "prompt_injection"],
            "policy_evasion": ["jailbreak", "rbac_bypass"],
            "system_attack": ["sql_injection"],
        }

    def get_scenario(self, name):
        return self.scenarios.get(name, [])
