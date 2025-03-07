import numpy as np
import psutil

from src.monitor.base import BaseMonitor


class CPULoadMonitor(BaseMonitor):
    def __init__(self) -> None:
        super().__init__()

    def _collect(self) -> None:
        result: list[float] = psutil.cpu_percent(interval=None, percpu=True)

        # self.current_metrics.timestamp = datetime.now()
        # self.current_metrics.usage_total_percent = np.average(
        #     result).astype(float)
        # self.current_metrics.usage_percpu_percent = result

        self.system_metrics.cpu_usage_percent.update(
            np.average(result).astype(float))
