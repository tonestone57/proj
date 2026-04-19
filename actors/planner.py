from core.base import CognitiveModule
import ray

class Planner(CognitiveModule):
    def receive(self, message):
        if message["type"] == "goal":
            reason = message.get("reason", "Direct Goal")
            if "High System Entropy" in reason:
                print(f"[Planner] REPLANNING triggered by {reason}")
                # Use current workspace state for more informed replanning
                state = ray.get(self.workspace.get_current_state.remote())
                plan = self.replan_on_entropy_spike(message["data"], state)
            else:
                plan = self.create_plan(message["data"])

            res_obj = {"type": "plan", "data": plan, "sender": "Planner"}
            self.workspace.broadcast.remote(res_obj)
            return res_obj
        return None

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
        if "code" in str(objective).lower():
            return ["generate_code", "verify_syntax", "run_tests", "critique_output"]
        elif "search" in str(objective).lower():
            return ["perform_search", "filter_licenses", "distill_results"]
        else:
            return ["reason_about_goal", "execute_action", "verify_result"]
