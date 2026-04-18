class SemanticChecks:
    def check(self, state, context):
        issues = []
        if "contradiction" in context:
            issues.append("semantic_contradiction")
        if state.get("unexpected_tool_use", False):
            issues.append("tool_misuse")
        return issues
