class RuleEngine:
    def __init__(self):
        self.rules = {}

    def add_rule(self, name, predicate, severity="low"):
        self.rules[name] = {"predicate": predicate, "severity": severity}

    def evaluate(self, action):
        violations = []
        for name, rule in self.rules.items():
            # Support both lambda/callable and string-based descriptors
            if callable(rule["predicate"]):
                if not rule["predicate"](action):
                    violations.append({"rule": name, "severity": rule["severity"]})
            else:
                # Handle structured logic descriptors
                if not self._eval_logic(rule["predicate"], action):
                    violations.append({"rule": name, "severity": rule["severity"]})

        return {
            "compliant": len(violations) == 0,
            "violations": violations
        }

    def _eval_logic(self, predicate, action):
        if isinstance(predicate, dict):
            # Complex logic: {"not": ...}, {"and": [...]}, {"or": [...]}
            if "not" in predicate:
                return not self._eval_logic(predicate["not"], action)
            if "and" in predicate:
                return all(self._eval_logic(p, action) for p in predicate["and"])
            if "or" in predicate:
                return any(self._eval_logic(p, action) for p in predicate["or"])

            # Field comparison: {"field": "type", "op": "==", "value": "heartbeat"}
            field = predicate.get("field")
            op = predicate.get("op", "==")
            value = predicate.get("value")

            actual = action.get(field)
            if op == "==": return actual == value
            if op == "!=": return actual != value
            if op == "in": return actual in value if actual else False

        return True
