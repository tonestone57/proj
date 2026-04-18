class MetaReasoner:
    def evaluate_reasoning(self, reasoning_trace):
        if not reasoning_trace:
            return {"quality": "unknown", "issues": ["empty_trace"]}

        issues = []
        if any("contradiction" in step for step in reasoning_trace):
            issues.append("logical_contradiction")

        return {
            "quality": "good" if not issues else "problematic",
            "issues": issues
        }
