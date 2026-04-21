import math
from core.config import THRESHOLD_REPLAN, THRESHOLD_CONSOLIDATE

def calculate_entropy(state):
    """
    Calculates the entropy of the system state based on message history.
    Formula: S = - sum P(xi) log P(xi)
    Now enhanced to consider message data complexity.
    """
    history = state.get("history", [])
    if not history:
        return 1.0  # High entropy for empty state

    # Count occurrences of different message types and track data keys
    type_counts = {}
    data_keys_all = set()
    for msg in history:
        if isinstance(msg, dict):
            msg_type = msg.get("type", "unknown")
            # Track unique keys in message data for complexity
            data = msg.get("data")
            if isinstance(data, dict):
                data_keys_all.update(data.keys())
        else:
            msg_type = str(type(msg))

        type_counts[msg_type] = type_counts.get(msg_type, 0) + 1

    total = len(history)
    entropy = 0
    for count in type_counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    # Add complexity factor based on diversity of data keys
    if data_keys_all:
        complexity = math.log2(len(data_keys_all) + 1) * 0.1
        entropy += complexity

    return entropy

class PIDController:
    """
    SGI 2026: Proportional-Integral-Derivative (PID) controller for thermal management.
    Maintains CPU temperature by calculating a stutter interval (duty cycle adjustment).
    """
    def __init__(self, setpoint=72.0, kp=0.01, ki=0.005, kd=0.001):
        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = 0.0
        self.last_time = None

    def update(self, current_value, dt=1.0):
        """
        Returns the control output (stutter interval in seconds).
        """
        error = current_value - self.setpoint
        self.integral += error * dt
        # Clamp integral to prevent windup
        self.integral = max(min(self.integral, 10.0), -10.0)

        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        # Output is stutter interval, must be non-negative
        return max(0.0, output)

class DriveEngine:
    def __init__(self):
        self.entropy = 0.0

    def evaluate_state(self, state):
        self.entropy = calculate_entropy(state)
        return self.entropy

    def update_objective_priorities(self):
        # Placeholder for dynamic priority updates based on drives
        pass
