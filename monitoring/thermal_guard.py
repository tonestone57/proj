import ray
import psutil
import time

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
        load = psutil.cpu_percent(interval=None)

        # Attempt to get temperature (OS dependent)
        temp = 0.0
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                temp = temps['coretemp'][0].current
            elif 'cpu_thermal' in temps:
                temp = temps['cpu_thermal'][0].current
        except Exception:
            pass

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
