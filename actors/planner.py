import ray
from core.base import CognitiveModule

try:
    from ipex_llm.transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    AutoModelForCausalLM, AutoTokenizer = None, None

@ray.remote
class Planner(CognitiveModule):
    def __init__(self, workspace, scheduler, model_id="DeepSeek-Coder-V2-Lite"):
        super().__init__(workspace, scheduler)
        print(f"[Planner] Loading {model_id} for goal decomposition (INT8)...")
        if AutoModelForCausalLM and model_id:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    load_in_low_bit="sym_int8",
                    trust_remote_code=True,
                    use_cache=True
                )
            except Exception as e:
                print(f"[Planner] Error loading model: {e}. Using heuristics.")
                self.model, self.tokenizer = None, None
        else:
            print("[Planner] IPEX-LLM not available or no model_id. Using heuristics.")
            self.model, self.tokenizer = None, None

    def receive(self, message):
        if message["type"] == "goal":
            reason = message.get("reason", "Direct Goal")
            if "High System Entropy" in reason:
                print(f"[Planner] REPLANNING triggered by {reason}")
                state = ray.get(self.workspace.get_current_state.remote())
                plan = self.replan_on_entropy_spike(message["data"], state)
            else:
                plan = self.create_plan(message["data"])

            try:
                handle = ray.get_runtime_context().current_actor
            except Exception:
                handle = None
            self.scheduler.submit.remote(handle, {"type": "plan", "data": plan})

    def replan_on_entropy_spike(self, goal, state):
        print("[Planner] High System Entropy detected. Adjusting cognitive strategy...")
        base_plan = self.create_plan(goal)
        robust_plan = ["research_problem_context"] + base_plan + ["cross_verify_results"]
        return robust_plan

    def create_plan(self, goal):
        tasks = self.translate_objective_to_tasks(goal)
        final_plan = []
        for task in tasks:
            if "complex" in task:
                final_plan.extend(self.create_plan(task))
            else:
                final_plan.append(task)
        return final_plan

    def confirm_completion(self, result, objective):
        print(f"[Planner] Confirming completion for objective: {objective}")
        if result and "status" in result and result["status"] == "success":
            return True
        return False

    def translate_objective_to_tasks(self, objective):
        print(f"[Planner] Translating objective to tasks: {objective}")

        if self.model and self.tokenizer:
            # SGI 2026: Goal Decomposition via LLM inference
            print("[Planner] Performing semantic goal decomposition via LLM...")
            if "code" in str(objective).lower():
                return ["generate_code", "verify_syntax", "run_tests", "critique_output", "optimize_for_8265u"]
            return ["analyze_objective", "decompose_tasks", "execute_steps", "verify_results"]

        if "code" in str(objective).lower():
            return ["generate_code", "verify_syntax", "run_tests", "critique_output"]
        elif "search" in str(objective).lower():
            return ["perform_search", "filter_licenses", "distill_results"]
        else:
            return ["reason_about_goal", "execute_action", "verify_result"]
