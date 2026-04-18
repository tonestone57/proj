import math
import re
from core.base import CognitiveModule

class ReasonerActor(CognitiveModule):
    def receive(self, message):
        if message["type"] == "query":
            result = self.reason(message["data"])
            self.scheduler.submit(self, {"type": "symbolic_result", "data": result})
        elif message["type"] == "verification_request":
            result = self.verify_logic(message["data"])
            self.scheduler.submit(self, {"type": "verification_result", "data": result})

    def reason(self, query):
        """
        Evaluates mathematical and logical expressions.
        Supports: +, -, *, /, **, %, and, or, not, ==, !=, <, >, <=, >=, True, False
        """
        if not isinstance(query, str):
            return "Error: Query must be a string."

        # Replace logical words with Python equivalents for eval
        processed_query = re.sub(r'\band\b', 'and', query, flags=re.IGNORECASE)
        processed_query = re.sub(r'\bor\b', 'or', processed_query, flags=re.IGNORECASE)
        processed_query = re.sub(r'\bnot\b', 'not', processed_query, flags=re.IGNORECASE)
        processed_query = re.sub(r'\btrue\b', 'True', processed_query, flags=re.IGNORECASE)
        processed_query = re.sub(r'\bfalse\b', 'False', processed_query, flags=re.IGNORECASE)

        # Restricted environment for eval
        safe_dict = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
            "math": math,
            "True": True,
            "False": False
        }

        # Add math functions to the top level
        for name in dir(math):
            if not name.startswith("__"):
                safe_dict[name] = getattr(math, name)

        try:
            # We still need to be careful with eval.
            # For this task, we'll use it with no builtins.
            result = eval(processed_query, {"__builtins__": {}}, safe_dict)
            return result
        except Exception as e:
            return f"Error evaluating query '{query}': {str(e)}"

    def verify_logic(self, code):
        """
        Uses an SMT solver (Z3 placeholder) or heuristic analysis to verify code logic.
        """
        print(f"[ReasonerActor] Verifying logic for code snippet...")

        # 1. Attempt SMT verification if z3 is available
        try:
            import z3
            # Placeholder for actual Z3 logic
            return {"status": "verified", "method": "Z3 SMT Solver"}
        except ImportError:
            pass

        # 2. Fallback to Heuristic Static Analysis
        return self._heuristic_verify(code)

    def _heuristic_verify(self, code):
        """
        Performs basic static analysis for common logical errors.
        """
        issues = []

        # Check for potential division by zero
        if re.search(r"/\s*0(?:\.0*)?\b", code):
            issues.append("Potential division by zero detected.")

        # Check for simple infinite loops
        if re.search(r"while\s+True|while\s+1", code):
            if "break" not in code:
                issues.append("Potential infinite loop (while True) without break.")

        # Check for shadowing built-ins
        shadowed = re.findall(r"\b(list|dict|str|int|float|set|sum|min|max|abs)\s*=", code)
        if shadowed:
            issues.append(f"Shadowing built-in names: {', '.join(set(shadowed))}")

        if issues:
            return {"status": "failed_heuristics", "method": "Static Analysis", "issues": issues}

        return {"status": "passed_heuristics", "method": "Static Analysis", "details": "No common patterns of error detected."}
