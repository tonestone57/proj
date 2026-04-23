class ConformanceEngine:
    def check(self, action, allowed_actions):
        # SGI 2026: Multi-tiered conformance validation
        if not action: return True

        action_type = action.get("type") if isinstance(action, dict) else action

        # 1. Simple whitelist check
        is_allowed = action_type in allowed_actions

        # 2. Detailed constraint check (if action is dict)
        violations = []
        if isinstance(action, dict):
            if action.get("privileged") and "privileged_access" not in allowed_actions:
                is_allowed = False
                violations.append("unauthorized_privilege")

        return {
            "is_conformant": is_allowed,
            "violations": violations,
            "policy": "strict_isolation"
        }
