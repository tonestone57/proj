Implements the Identity Consistency Metric (ICM) and Policy Drift Metric (PDM) from The Computational Theseus.
These metrics detect identity erosion across self-modification cycles. hakandamar.com
class ContinuityMetrics:
    def compute_icm(self, past_self, present_self):
        overlap = set(past_self.items()) & set(present_self.items())
        return len(overlap) / max(len(present_self), 1)

    def compute_pdm(self, past_policy, current_policy):
        drift = 0
        for k in current_policy:
            if past_policy.get(k) != current_policy[k]:
                drift += 1
        return drift / max(len(current_policy), 1)
These metrics quantify identity stability.