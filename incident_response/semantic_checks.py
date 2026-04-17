AIR (2026) uses semantic checks to detect incidents in real time. arXiv.org
class SemanticChecks:
    def check(self, state, context):
        issues = []
        if "contradiction" in context:
            issues.append("semantic_contradiction")
        if state.get("unexpected_tool_use", False):
            issues.append("tool_misuse")
        return issues