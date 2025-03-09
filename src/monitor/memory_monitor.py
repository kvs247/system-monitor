import psutil

from src.monitor.base import BaseMonitor
from src.utils import bytes_to_gib


class MemoryMonitor(BaseMonitor):
    def __init__(self) -> None:
        super().__init__()

    def _collect(self) -> None:
        mem = psutil.virtual_memory()
        self.system_metrics.memory_usage_percent.update(mem.percent)
        self.system_metrics.memory_used_gib.update(bytes_to_gib(mem.used))
        self.system_metrics.memory_free_gib.update(bytes_to_gib(mem.available))

        swap = psutil.swap_memory()
        self.system_metrics.swap_usage_percent.update(
            bytes_to_gib(swap.percent))
        self.system_metrics.swap_used_gib.update(bytes_to_gib(swap.used))
        self.system_metrics.swap_free_gib.update(bytes_to_gib(swap.free))
