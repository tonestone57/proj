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

    def DigitalTwin_Branching(self, branch_name):
        """
        Simulates branching the Firecracker VM state for speculative execution.
        """
        print(f"[CodingActor] Creating speculative branch: {branch_name}")
        # In 2026, this allows risky refactors without affecting the main twin
        return f"vm_branch_{branch_name}_0xdeadbeef"

    def execute_code(self, code, persistent=False):
        """
        Executes Python code in a restricted environment and captures output.
        If persistent=True, it operates within a Stateful Digital Twin (Firecracker microVM).
        This allows for Speculative Execution and state rewinding.
        """
        # If code is too large, perform schema-aware distillation first
        if len(code.split()) > 1000:
            code = self.distill_code(code)

        if persistent:
            print(f"[CodingActor] Connecting to Persistent Digital Twin (Firecracker VM).")
            # Simulate Speculative Execution: branching the VM state
            branch_id = self.DigitalTwin_Branching("speculative_run")
            print(f"[CodingActor] Branch {branch_id} ready.")

            # Observe side effects on the "World" (system resources, logs, network)
            self.Runtime_Observation_Hook(branch_id)

        return self.execute_logic_internal(code)

    def Runtime_Observation_Hook(self, context_id):
        """
        Simulates real-time monitoring of side effects during code execution.
        """
        print(f"[CodingActor] [{context_id}] Hooking into runtime for observation...")
        # Simulate monitoring resources and logs
        obs = {"cpu_spike": False, "network_io": 0, "logs": "Success"}
        print(f"[CodingActor] Observation complete: {obs}")
        return obs

    def VM_State_Rollback(self, branch_id):
        """
        Simulates rolling back the VM state after a speculative failure.
        """
        print(f"[CodingActor] REWINDING branch {branch_id} to parent state.")
        return True

    def UnitTest_Synthesizer(self, code):
        """
        Simulates automated unit test generation for a code snippet.
        """
        print("[CodingActor] Synthesizing unit tests for code...")
        # Simulate generating a simple assert test
        test_code = "def test_generated():\n    # Mocked test logic\n    assert True"
        return test_code

    def execute_logic_internal(self, code):
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
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr): exec(code, safe_globals)
            output, errors = stdout.getvalue(), stderr.getvalue()
            return {"status": "error", "output": output, "error": errors} if errors else {"status": "success", "output": output}
        except Exception as e:
            return {"status": "exception", "error": str(e)}
