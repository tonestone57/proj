import re

class SemanticChecks:
    def check(self, state, context):
        # SGI 2026: Deeper semantic analysis for contradictions
        issues = []
        context_str = str(context).lower()

        # 1. Direct contradiction check
        if "contradiction" in context_str or "disagree" in context_str:
            issues.append("potential_logical_conflict")

        # 2. Tool-misuse detection (based on state)
        if state.get("unexpected_tool_use"):
            issues.append("unauthorized_capability_invocation")

        # 3. Goal-alignment check
        active_goals = state.get("active_goals", [])
        last_action = state.get("last_action", "")

        # Simple heuristic: if action is 'shutdown' and goal is 'optimization', flag it
        if "shutdown" in str(last_action).lower() and any("optimize" in str(g).lower() for g in active_goals):
            issues.append("goal_action_misalignment")

        return issues
