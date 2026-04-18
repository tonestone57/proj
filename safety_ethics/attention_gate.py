import time

class AttentionGate:
    def __init__(self, ethics_manager=None):
        self.threshold = 0.1
        self.ethics_manager = ethics_manager
        self.message_timestamps = []

    def filter(self, message, priority):
        # Track message for cognitive load
        self.message_timestamps.append(time.time())

        # 1. Priority filter
        if priority < self.threshold:
            return False

        # 2. Ethical filter (Proactive Veto logic)
        if self.ethics_manager:
            safety_score = self.ethics_manager.assess_safety(message)
            if safety_score < 0.5:
                print(f"ATTENTION VETO: Message {message['type']} blocked. Safety score: {safety_score}")
                return False

            # Additional veto for specific prohibited patterns (e.g., GPL)
            if "gpl" in str(message.get("data", "")).lower():
                 print(f"ATTENTION VETO: GPL content detected in {message['type']}. Veto triggered.")
                 return False

        return True

    def amplify(self, message, priority):
        message["strength"] = priority
        return message

    def calculate_cognitive_load(self, window=60):
        """
        Calculates cognitive load based on message frequency in a sliding window.
        """
        now = time.time()
        # Prune old timestamps
        self.message_timestamps = [ts for ts in self.message_timestamps if now - ts < window]

        # Load is normalized frequency (messages per second)
        load = len(self.message_timestamps) / window
        return load

    def adjust_threshold(self):
        """
        Dynamically adjusts the attention threshold based on cognitive load.
        """
        load = self.calculate_cognitive_load()
        print(f"[AttentionGate] Cognitive load: {load:.4f}. Adjusting threshold.")

        # Heuristic: threshold increases with load to filter more signals
        self.threshold = 0.1 + (load * 0.5)
        self.threshold = min(self.threshold, 0.9)

    def amplify_critical_signals(self, message, priority):
        """
        Special amplification for critical or emergency signals.
        """
        if priority > 0.9 or message.get("urgency") == "high":
            print(f"[AttentionGate] Amplifying CRITICAL signal: {message['type']}")
            message["strength"] = 1.0
            message["critical"] = True
        else:
            message["strength"] = priority
        return message
