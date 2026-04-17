Implements joint utility consistent with MARL-based RAO frameworks.
class UtilityEngine:
    def compute(self, allocation, demand):
        return max(0, 1 - abs(allocation - demand))