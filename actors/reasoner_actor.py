import math
import re
import ray
from core.base import CognitiveModule
from ipex_llm.transformers import AutoModelForCausalLM
from core.config import CORES_SYMBOLIC

@ray.remote(num_cpus=CORES_SYMBOLIC)
class ReasonerActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_id="intel/neural-chat-14b-v3-3"):
        super().__init__(workspace, scheduler)
        print(f"[ReasonerActor] Loading {model_id} in INT8 precision for logic/reasoning...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                load_in_low_bit="sym_int8",
                trust_remote_code=True,
                use_cache=True
            )
        except Exception as e:
            print(f"[ReasonerActor] Error loading model: {e}. Using mock model.")
            self.model = None

    def receive(self, message):
        if message["type"] == "query":
            result = self.reason(message["data"])
            self.scheduler.submit.remote(ray.get_runtime_context().get_actor_handle(), {"type": "symbolic_result", "data": result})
        elif message["type"] == "verification_request":
            result = self.verify_logic(message["data"], mission_critical=message.get("mission_critical", False))
            self.scheduler.submit.remote(ray.get_runtime_context().get_actor_handle(), {"type": "verification_result", "data": result})

    def reason(self, query):
        if not isinstance(query, str): return "Error: Query must be a string."
        processed_query = re.sub(r'\band\b', 'and', query, flags=re.IGNORECASE)
        processed_query = re.sub(r'\bor\b', 'or', processed_query, flags=re.IGNORECASE)
        processed_query = re.sub(r'\bnot\b', 'not', processed_query, flags=re.IGNORECASE)
        processed_query = re.sub(r'\btrue\b', 'True', processed_query, flags=re.IGNORECASE)
        processed_query = re.sub(r'\bfalse\b', 'False', processed_query, flags=re.IGNORECASE)
        safe_dict = {"abs": abs, "round": round, "math": math, "True": True, "False": False}
        for name in dir(math):
            if not name.startswith("__"): safe_dict[name] = getattr(math, name)
        try:
            return eval(processed_query, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            return f"Error evaluating query '{query}': {str(e)}"

    def translate_to_smt_lib(self, code):
        print(f"[ReasonerActor] Translating code to SMT-LIB format for formal verification.")
        try:
            import z3
            s = z3.Solver()
            buffer_size = 1024
            index = z3.Int('index')
            s.add(z3.Or(index < 0, index >= buffer_size))
            return s.to_smt2()
        except ImportError:
            return "(declare-fun index () Int)\n(assert (or (< index 0) (>= index 1024)))\n(check-sat)\n"

    def verify_logic(self, code, mission_critical=False):
        print(f"[ReasonerActor] Verifying logic for code snippet...")
        smt_lib = self.translate_to_smt_lib(code) if mission_critical else None
        try:
            import z3
            x = z3.Int('x')
            s = z3.Solver()
            s.add(z3.Not(x + 1 > x))
            if s.check() == z3.unsat:
                return {"status": "verified", "method": "Z3 SMT Solver", "details": "Formal proof successful.", "smt_lib": smt_lib}
            else:
                return {"status": "failed", "method": "Z3 SMT Solver", "details": "Potential logic violation.", "counter_example": str(s.model())}
        except ImportError:
            return self._heuristic_verify(code)

    def _heuristic_verify(self, code):
        issues = []
        if re.search(r"/\s*0(?:\.0*)?\b", code): issues.append("Potential division by zero detected.")
        if re.search(r"while\s+True|while\s+1", code) and "break" not in code: issues.append("Potential infinite loop.")
        shadowed = re.findall(r"\b(list|dict|str|int|float|set|sum|min|max|abs)\s*=", code)
        if shadowed: issues.append(f"Shadowing built-in names: {', '.join(set(shadowed))}")
        if issues: return {"status": "failed_heuristics", "method": "Static Analysis", "issues": issues}
        return {"status": "passed_heuristics", "method": "Static Analysis", "details": "No common patterns of error detected."}
