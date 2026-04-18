from self_model.identity_kernel import IdentityKernel
from self_model.autobiographical_memory import AutobiographicalMemory
from self_model.temporal_self import TemporalSelf
from self_model.continuity_metrics import ContinuityMetrics
from self_model.reflective_endorsement import ReflectiveEndorsement

class SelfManager:
    def __init__(self):
        self.kernel = IdentityKernel()
        self.memory = AutobiographicalMemory()
        self.temporal = TemporalSelf()
        self.metrics = ContinuityMetrics()
        self.endorsement = ReflectiveEndorsement()
        self.last_policy = {}

    def update_self(self, state, policy):
        self.temporal.update_present(state)
        self.memory.store_episode({"state": state, "policy": policy})

        icm = self.metrics.compute_icm(self.temporal.past_self, state)
        pdm = self.metrics.compute_pdm(self.last_policy, policy)

        self.temporal.record_past()
        self.last_policy = policy.copy()

        return {"ICM": icm, "PDM": pdm}

    def approve_update(self, proposed_update):
        return self.endorsement.endorse(self.kernel, proposed_update)
