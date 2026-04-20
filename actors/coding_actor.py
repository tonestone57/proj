import sys
import io
import contextlib
import ray
from core.base import CognitiveModule
from core.config import CORES_CODING

@ray.remote(num_cpus=CORES_CODING)
@ray.remote
class CodingActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        print(f"[CodingActor] Initialized. Using Shared Model Provider for coding tasks...")

    def receive(self, message):
        if message["type"] == "code_execution":
            code = message["data"]
            persistent = message.get("persistent", False)
            confidence = self.calculate_confidence_score()

            if confidence < 0.4:
                self.scheduler.submit.remote(None, {
                    "type": "search_request",
                    "data": f"Docs for: {code[:50]}",
                    "reason": "Low Confidence"
                })

            if self.model_registry and "generate" in message.get("mode", ""):
                result = {"status": "success", "output": ray.get(self.model_registry.generate.remote(code))}
            else:
                result = self.execute_code(code, persistent=persistent)
            result["confidence"] = confidence

            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None
            self.scheduler.submit.remote(handle, {"type": "code_result", "data": result})

    def calculate_confidence_score(self):
        from core.drives import calculate_entropy
        state = ray.get(self.workspace.get_current_state.remote())
        entropy = calculate_entropy(state)
        return max(0.0, 1.0 - (entropy / 5.0))

    def DigitalTwin_Branching(self, branch_name):
        print(f"[CodingActor] Creating speculative branch: {branch_name}")
        return f"vm_branch_{branch_name}_0xdeadbeef"

    def execute_code(self, code, persistent=False):
        if persistent:
            from world_model.state import VMStateDigitalTwin
            twin = VMStateDigitalTwin(vm_id="speculative-01")
            twin.start()
            branch_id = self.DigitalTwin_Branching("speculative_run")
            twin.branch(branch_id)
        return self.execute_logic_internal(code)

    def execute_logic_internal(self, code):
        stdout, stderr = io.StringIO(), io.StringIO()
        safe_globals = {"__builtins__": {"print": print, "range": range, "len": len, "int": int, "str": str}}
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(code, safe_globals)
            return {"status": "success", "output": stdout.getvalue()}
        except Exception as e:
            return {"status": "exception", "error": str(e)}
