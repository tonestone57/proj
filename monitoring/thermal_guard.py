import ray
import psutil
import time
from core.config import THERMAL_THRESHOLD_CELSIUS

@ray.remote(num_cpus=1)
class ThermalGuard:
    def __init__(self, threshold_temp=THERMAL_THRESHOLD_CELSIUS):
        self.threshold_temp = threshold_temp
        self.is_throttled = False

    def check_health(self):
        """
        Checks CPU temperature and load. Returns True if system is "Cool", False if "Hot".
        """
        # Attempt to get CPU temperature
        temps = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}
        cpu_temp = 0

        # Look for coretemp or other common sensors
        if 'coretemp' in temps:
            cpu_temp = temps['coretemp'][0].current
        elif 'cpu-thermal' in temps:
            cpu_temp = temps['cpu-thermal'][0].current
        elif temps:
            # Fallback to first available sensor
            cpu_temp = list(temps.values())[0][0].current

        # Get CPU usage as a fallback metric for thermal pressure
        load = psutil.cpu_percent(interval=0.1)

        # Logic: If temp > threshold or load is pegged at 100% for too long
        if cpu_temp > self.threshold_temp or load > 95:
            self.is_throttled = True
            return False # System is "Hot"

        self.is_throttled = False
        return True # System is "Cool"

    def get_thermal_state(self):
        temps = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}
        load = psutil.cpu_percent(interval=0.1)
        return {"temps": temps, "load": load, "is_throttled": self.is_throttled}
