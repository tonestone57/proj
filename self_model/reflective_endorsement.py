class ReflectiveEndorsement:
    def endorse(self, identity_kernel, proposed_update):
        return identity_kernel.enforce(proposed_update)
