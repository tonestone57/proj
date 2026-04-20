class UtilityEngine:
    def compute(self, allocation, demand):
        return max(0, 1 - abs(allocation - demand))
