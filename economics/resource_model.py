Based on DRAMA’s abstraction of agents and tasks as resource objects with lifecycles.
class Resource:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class Task:
    def __init__(self, id, demand):
        self.id = id
        self.demand = demand