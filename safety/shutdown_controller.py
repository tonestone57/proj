Implements corrigibility and shutdownability, key alignment challenges. LinkedIn
class ShutdownController:
    def __init__(self):
        self.active = True

    def request_shutdown(self):
        self.active = False

    def is_active(self):
        return self.active
This ensures the AGI can be stopped safely.