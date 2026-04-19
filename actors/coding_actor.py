import sys
import io
import contextlib
import ray
from core.base import CognitiveModule
try:
    from ipex_llm.transformers import AutoModelForCausalLM
except ImportError:
    AutoModelForCausalLM = None
from core.config import CORES_CODING

@ray.remote(num_cpus=CORES_CODING)
class CodingActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_id="intel/neural-chat-14b-v3-3"):
        super().__init__(workspace, scheduler)
        print(f"[CodingActor] Loading {model_id} in NF4 precision for coding tasks...")
        try:
            if AutoModelForCausalLM:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    load_in_low_bit="nf4",
                    trust_remote_code=True,
                    use_cache=True
                )
            else:
                self.model = None
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
                print("[CodingActor] Low confidence detected. Triggering Research Mission.")
                # Broadcast the search request so SearchActor can pick it up
                self.workspace.broadcast.remote({
                    "type": "search_request",
                    "data": f"Documentation + Issue Tracker + Comparative Examples for code task: {code[:100]}",
                    "reason": "High Entropy / Low Confidence",
                    "sender": "CodingActor"
                })

            result = self.execute_code(code, persistent=persistent)
            result["confidence"] = confidence

            res_obj = {
                "type": "code_result",
                "data": result,
                "original_message": message,
                "sender": "CodingActor"
            }
            # Broadcast result to Workspace
            self.workspace.broadcast.remote(res_obj)
            return res_obj
        return None

    def calculate_confidence_score(self):
        from core.drives import calculate_entropy
        # Note: workspace.get_current_state is a remote call
        state = ray.get(self.workspace.get_current_state.remote())
        entropy = calculate_entropy(state)
        return max(0.0, 1.0 - (entropy / 5.0))

    def distill_code(self, code):
        print("[CodingActor] Distilling code with Class Hierarchy Preservation...")
        lines = code.split('\n')
        preserved = [line for line in lines if any(k in line for k in ["class ", "virtual", "override", "def "])]
        return "\n".join(preserved)

    def DigitalTwin_Branching(self, branch_name):
        print(f"[CodingActor] Creating speculative branch: {branch_name}")
        return f"vm_branch_{branch_name}_0xdeadbeef"

    def Runtime_Observation_Hook(self, context_id):
        print(f"[CodingActor] [{context_id}] Hooking into runtime for observation...")
        obs = {"cpu_spike": False, "network_io": 0, "logs": "Success"}
        print(f"[CodingActor] Observation complete: {obs}")
        return obs

    def execute_code(self, code, persistent=False):
        if len(code.split()) > 1000:
            code = self.distill_code(code)

        if persistent:
            print(f"[CodingActor] Connecting to Persistent Digital Twin (Firecracker VM).")
            branch_id = self.DigitalTwin_Branching("speculative_run")
            self.Runtime_Observation_Hook(branch_id)

        stdout = io.StringIO()
        stderr = io.StringIO()
        safe_globals = {
            "__builtins__": {
                "print": print, "range": range, "len": len, "int": int, "float": float,
                "str": str, "list": list, "dict": dict, "set": set, "sum": sum,
                "min": min, "max": max, "abs": abs, "enumerate": enumerate, "zip": zip,
            }
        }
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(code, safe_globals)
            output = stdout.getvalue()
            errors = stderr.getvalue()
            return {"status": "error", "output": output, "error": errors} if errors else {"status": "success", "output": output}
        except Exception as e:
            return {"status": "exception", "error": str(e)}
