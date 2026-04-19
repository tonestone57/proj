from core.base import CognitiveModule

class CriticActor(CognitiveModule):
    """
    Evaluates the outputs of other actors to ensure accuracy, safety, and goal alignment.
    Acts as an 'Internal Critic' to verify reasoning before finalization.
    """
    def __init__(self, workspace, scheduler):
        super().__init__(workspace, scheduler)
        self.critiques = []

    def critique_code(self, code):
        """
        Evaluates syntax, style, and potential bugs in generated code.
        """
        print(f"[CriticActor] Critiquing code snippet...")
        issues = []
        if len(code) < 10:
            issues.append("Code snippet is suspiciously short.")
        if "TODO" in code:
            issues.append("Code contains unfinished placeholders (TODO).")

        # Simple syntax heuristic
        if code.count("(") != code.count(")"):
            issues.append("Mismatched parentheses detected.")

        return issues

    def critique_logic(self, reasoning):
        """
        Reviews mathematical and symbolic reasoning for consistency.
        """
        print(f"[CriticActor] Critiquing symbolic reasoning...")
        issues = []
        if "1/0" in reasoning or "division by zero" in reasoning.lower():
            issues.append("Logic contains potential division by zero.")
        if "True == False" in reasoning:
            issues.append("Blatant logical contradiction detected.")

        return issues

    def verify_goal_alignment(self, output, goal):
        """
        Ensures output matches the original objective from the Planner.
        """
        print(f"[CriticActor] Verifying alignment with goal: {goal}")
        # Simple keyword-based alignment check
        goal_keywords = set(str(goal).lower().split())
        output_keywords = set(str(output).lower().split())

        overlap = goal_keywords.intersection(output_keywords)
        if not overlap:
            return ["Output does not appear to address the specified goal."]
        return []

    def receive(self, message):
        if message["type"] == "critique_request":
            data = message["data"]
            category = message.get("category", "general")

            issues = []
            if category == "code":
                issues = self.critique_code(data)
            elif category == "logic":
                issues = self.critique_logic(data)

            # Check alignment if goal is provided
            if "goal" in message:
                issues.extend(self.verify_goal_alignment(data, message["goal"]))

            self.scheduler.submit(self, {
                "type": "critique_result",
                "issues": issues,
                "original_sender": message.get("sender")
            })
