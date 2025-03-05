import psutil
import numpy as np

from datetime import datetime
from dataclasses import dataclass
from monitor.base import BaseMonitor


@dataclass
class CPULoadMetrics:
    timestamp: datetime
    usage_total: float
    usage_percpu: list[float]


class CPULoadMonitor(BaseMonitor[CPULoadMetrics]):
    def __init__(self) -> None:
        super().__init__()

    def _init_current_metrics(self) -> CPULoadMetrics:
        return CPULoadMetrics(timestamp=datetime.now(),
                              usage_total=0.0, usage_percpu=[])

    def _collect(self) -> None:
        result: list[float] = psutil.cpu_percent(interval=None, percpu=True)

        self.current_metrics.timestamp = datetime.now()
        self.current_metrics.usage_total = np.average(result).astype(float)
        self.current_metrics.usage_percpu = result
