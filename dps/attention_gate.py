class AttentionGate:
    def __init__(self, ethics_manager=None):
        self.threshold = 0.1
        self.ethics_manager = ethics_manager

    def filter(self, message, priority):
        # 1. Priority filter
        if priority < self.threshold:
            return False

        # 2. Ethical filter (Veto logic)
        if self.ethics_manager:
            if not self.ethics_manager.is_safe(message):
                print(f"ATTENTION VETO: Message of type {message['type']} blocked by ethics.")
                return False

        return True

    def amplify(self, message, priority):
        message["strength"] = priority
        return message
