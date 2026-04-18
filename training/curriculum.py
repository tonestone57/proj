class Curriculum:
    def __init__(self):
        self.level = 0
        self.thresholds = [10, 20, 40, 80]

    def update(self, performance):
        if performance > self.thresholds[self.level]:
            self.level = min(self.level + 1, len(self.thresholds) - 1)

    def get_current_tasks(self):
        return {
            0: ["simple perception"],
            1: ["basic planning"],
            2: ["multi-step reasoning"],
            3: ["social inference"],
        }[self.level]
