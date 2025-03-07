import psutil

from src.monitor.base import BaseMonitor
from utils import bytes_to_gib


class MemoryMonitor(BaseMonitor):
    def __init__(self) -> None:
        super().__init__()

    def _collect(self) -> None:
        mem = psutil.virtual_memory()
        # self.current_metrics.timestamp = datetime.now()
        # self.current_metrics.memory_used_percent = mem.percent
        # self.current_metrics.memory_used_gib = bytes_to_gib(mem.used)
        # self.current_metrics.memory_free_gib = bytes_to_gib(mem.available)

        swap = psutil.swap_memory()
        # self.current_metrics.timestamp = datetime.now()
        # self.current_metrics.swap_used_percent = swap.percent
        # self.current_metrics.swap_used_gib = bytes_to_gib(swap.used)
        # self.current_metrics.swap_free_gib = bytes_to_gib(swap.free)

        self.system_metrics.memory_usage_percent.update(mem.percent)
