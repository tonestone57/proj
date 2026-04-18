import math
import re
from core.base import CognitiveModule

class ReasonerActor(CognitiveModule):
    def receive(self, message):
        if message["type"] == "query":
            result = self.reason(message["data"])
            self.scheduler.submit(self, {"type": "symbolic_result", "data": result})

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
