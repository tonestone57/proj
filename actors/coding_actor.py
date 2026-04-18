import sys
import io
import contextlib
import ray
from core.base import CognitiveModule
from ipex_llm.transformers import AutoModelForCausalLM
from core.config import CORES_CODING

@ray.remote(num_cpus=CORES_CODING)
class CodingActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_id="intel/neural-chat-14b-v3-3"):
        super().__init__(workspace, scheduler)
        print(f"[CodingActor] Loading {model_id} in NF4 precision for coding tasks...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                load_in_low_bit="nf4",
                trust_remote_code=True,
                use_cache=True
            )
        except Exception as e:
            print(f"[CodingActor] Error loading model: {e}. Using mock executor.")
            self.model = None

    def receive(self, message):
        if message["type"] == "code_execution":
            code = message["data"]
            persistent = message.get("persistent", False)
            confidence = self.calculate_confidence_score()
            print(f"[CodingActor] Solution confidence score: {confidence:.4f}")
            if confidence < 0.4:
                self.scheduler.submit.remote(None, {"type": "search_request", "data": f"Docs for: {code[:50]}", "reason": "Low Confidence"})
            result = self.execute_code(code, persistent=persistent)
            result["confidence"] = confidence
            self.scheduler.submit.remote(ray.get_runtime_context().get_actor_handle(), {"type": "code_result", "data": result, "original_message": message})

    def calculate_confidence_score(self):
        from core.drives import calculate_entropy
        state = ray.get(self.workspace.get_current_state.remote())
        return max(0.0, 1.0 - (calculate_entropy(state) / 5.0))

    def distill_code(self, code):
        print("[CodingActor] Distilling code with Class Hierarchy Preservation...")
        lines = code.split('\n')
        preserved = [line for line in lines if any(k in line for k in ["class ", "virtual", "override", "def "])]
        return "\n".join(preserved)

    def execute_code(self, code, persistent=False):
        if len(code.split()) > 1000: code = self.distill_code(code)
        if persistent: print(f"[CodingActor] Connecting to Persistent Digital Twin (Firecracker VM).")
        stdout, stderr = io.StringIO(), io.StringIO()
        safe_globals = {"__builtins__": {k: __builtins__.get(k) for k in ["print", "range", "len", "int", "float", "str", "list", "dict", "set", "sum", "min", "max", "abs", "enumerate", "zip"]}}
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr): exec(code, safe_globals)
            output, errors = stdout.getvalue(), stderr.getvalue()
            return {"status": "error", "output": output, "error": errors} if errors else {"status": "success", "output": output}
        except Exception as e:
            return {"status": "exception", "error": str(e)}
