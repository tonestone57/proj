class AGIState:
    def __init__(self):
        self.beliefs = []
        self.memory = {}
        self.context = {}
        self.world_model = {}
        self.emotional_state = {}
        self.ethical_state = {}
        self.active_tasks = []
        self.last_action = None
