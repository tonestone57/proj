class EradicationEngine:
    def synthesize_rules(self, incident_type):
        if incident_type == "prompt_injection":
            return ["block_override_patterns"]
        if incident_type == "memory_poisoning":
            return ["validate_memory_sources"]
        return ["generic_hardening"]
