import numpy as np
import psutil

from src.monitor.base import BaseMonitor


class CPULoadMonitor(BaseMonitor):
    def __init__(self) -> None:
        super().__init__()

    def _collect(self) -> None:
        cpu_percent: list[float] = psutil.cpu_percent(
            interval=None, percpu=True)
        self.system_metrics.cpu_usage_percent.update(
            np.average(cpu_percent).astype(float))

        cpu_temp = psutil.sensors_temperatures()
        temps = cpu_temp["coretemp"]
        current_temps = [t.current for t in temps]

        self.system_metrics.cpu_temp_avg_c.update(
            np.average(current_temps).astype(float))
        self.system_metrics.cpu_temp_max_c.update(
            np.max(current_temps).astype(float))
