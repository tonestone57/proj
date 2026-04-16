Implements event-driven interrupts from EDA patterns.
LinkedIn
class InterruptHandler:
    def check_interrupt(self, event):
        return event.get("interrupt", False)