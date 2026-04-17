class WorkingMemory:
    def __init__(self):
        self.slots = {}

    def store(self, key, value):
        self.slots[key] = value

    def retrieve(self, key):
        return self.slots.get(key)