import sys
import io
import contextlib
from modules.base import CognitiveModule

class CodingModule(CognitiveModule):
    def receive(self, message):
        if message["type"] == "code_execution":
            code = message["data"]
            result = self.execute_code(code)
            self.scheduler.submit(self, {
                "type": "code_result",
                "data": result,
                "original_message": message
            })

    def execute_code(self, code):
        """
        Executes Python code in a restricted environment and captures output.
        """
        stdout = io.StringIO()
        stderr = io.StringIO()

        # Restricted globals
        safe_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "int": int,
                "float": float,
                "str": str,
                "list": list,
                "dict": dict,
                "set": set,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "enumerate": enumerate,
                "zip": zip,
            }
        }

        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(code, safe_globals)

            output = stdout.getvalue()
            errors = stderr.getvalue()

            if errors:
                return {"status": "error", "output": output, "error": errors}
            return {"status": "success", "output": output}

        except Exception as e:
            return {"status": "exception", "error": str(e)}
