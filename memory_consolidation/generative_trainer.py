class GenerativeTrainer:
    def __init__(self, generative_model):
        self.model = generative_model

    def train_on_replay(self, replay_batch):
        losses = []
        for sensory_input in replay_batch:
            loss = self.model.train_step(sensory_input)
            losses.append(loss)
        return sum(losses) / len(losses)
