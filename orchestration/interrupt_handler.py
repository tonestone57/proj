
class InterruptHandler:
    def __init__(self, threshold=0.8):
        self.critical_threshold = threshold

    def check_interrupt(self, event):
        # SGI 2026: Priority-based preemption
        if not event: return False

        is_hard_interrupt = event.get("interrupt", False)
        priority = event.get("priority", 0.0)

        # Immediate interrupt if hard flag is set or priority is critical
        if is_hard_interrupt or priority >= self.critical_threshold:
            print(f"[InterruptHandler] Preempting current task: {event.get('type')}")
            return True

        return False
