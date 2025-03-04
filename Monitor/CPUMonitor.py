import psutil
from Monitor.BaseMonitor import BaseMonitor


class CPUMonitor(BaseMonitor):
    def __init__(self):
        super().__init__()
        self.cpu_percent: float = 0

    def _collect(self) -> None:
        self.cpu_percent = psutil.cpu_percent(interval=1)
