class Curriculum:
    def __init__(self):
        self.level = 0
        self.thresholds = [10, 25, 50, 100]
        self.task_map = {
            0: ["simple_perception", "basic_syntax"],
            1: ["logic_synthesis", "basic_planning"],
            2: ["multi_step_reasoning", "strategic_alignment"],
            3: ["social_inference", "recursive_mdl_refactoring"]
        }

    def update(self, performance_metrics):
        # SGI 2026: Dynamic curriculum scaling
        if isinstance(performance_metrics, (int, float)):
            avg_score = float(performance_metrics)
        else:
            avg_score = performance_metrics.get("average_score", 0) if performance_metrics else 0

        if avg_score > self.thresholds[self.level]:
            if self.level < len(self.thresholds) - 1:
                self.level += 1
                print(f"[Curriculum] Scaling up to level {self.level}")
        elif avg_score < self.thresholds[self.level] * 0.5:
             if self.level > 0:
                self.level -= 1
                print(f"[Curriculum] Scaling down to level {self.level}")

    def get_current_tasks(self):
        return self.task_map.get(self.level, ["unknown"])

    def get_status(self):
        return {"current_level": self.level, "tasks": self.get_current_tasks()}
