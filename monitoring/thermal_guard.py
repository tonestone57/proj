import ray
import psutil
import math

@ray.remote
class ThermalGuard:
    def __init__(self, threshold_temp=78.0, threshold_load=95.0):
        self.threshold_temp = threshold_temp
        self.threshold_load = threshold_load
        print(f"[ThermalGuard] Initialized. Thresholds: {threshold_temp}C, {threshold_load}% Load")

    def get_thermal_state(self):
        """
        Monitors CPU temperature and load.
        Note: Temperature monitoring might require specific permissions or drivers.
        """
        try:
            load = psutil.cpu_percent(interval=None)
        except Exception:
            load = 0.0

        # Attempt to get temperature (OS dependent)
        temp = 45.0 # Default safe temperature
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if 'coretemp' in temps and temps['coretemp']:
                    temp = temps['coretemp'][0].current
                elif 'cpu_thermal' in temps and temps['cpu_thermal']:
                    temp = temps['cpu_thermal'][0].current
                elif 'acpitz' in temps and temps['acpitz']:
                    temp = temps['acpitz'][0].current
                elif not temps:
                    # Fallback heuristic: assume temp correlates with load if sensors fail
                    # SGI 2026: Refined heuristic for i7-8265U (15W TDP)
                    # Base idle ~38C, linear ramp with exponential bias at high load
                    temp = 38.0 + (load * 0.42) + (math.exp(load / 40.0) if load > 60 else 0)
            else:
                # Fallback heuristic for platforms without sensors_temperatures
                temp = 38.0 + (load * 0.42) + (math.exp(load / 40.0) if load > 60 else 0)
        except Exception:
            # Final fallback
            temp = 38.0 + (load * 0.42) + (math.exp(load / 40.0) if load > 60 else 0)

        is_throttled = temp > self.threshold_temp or load > self.threshold_load

        return {
            "temp": temp,
            "load": load,
            "is_throttled": is_throttled
        }

    def check_health(self):
        """
        Returns True if the system is within safe thermal/load limits.
        """
        state = self.get_thermal_state()
        if state["is_throttled"]:
            print(f"⚠️ [ThermalGuard] System Alert! Temp: {state['temp']}C, Load: {state['load']}%")
            return False
        return True
