class SelfSupervisedTrainer:
    def __init__(self, modules):
        self.modules = modules

    def train_step(self, data):
        losses = {}

        for name, module in self.modules.items():
            if hasattr(module, "self_supervised"):
                loss = module.self_supervised(data)
                losses[name] = loss

        return losses
