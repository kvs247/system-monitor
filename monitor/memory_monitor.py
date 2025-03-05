import psutil

from datetime import datetime
from dataclasses import dataclass
from monitor.base import BaseMonitor
from utils import bytes_to_gib


@dataclass
class MemoryMetrics:
    timestamp: datetime
    mem_used_percent: float
    mem_used_gib: float
    mem_free_gib: float
    swap_used_percent: float
    swap_used_gib: float
    swap_free_gib: float


class MemoryMonitor(BaseMonitor[MemoryMetrics]):
    def __init__(self) -> None:
        super().__init__()

    def _init_current_metrics(self) -> MemoryMetrics:
        return MemoryMetrics(
            timestamp=datetime.now(),
            mem_used_percent=0.0,
            mem_used_gib=0.0,
            mem_free_gib=0.0,
            swap_used_percent=0.0,
            swap_used_gib=0.0,
            swap_free_gib=0.0,
        )

    def _collect(self) -> None:
        mem = psutil.virtual_memory()
        self.current_metrics.timestamp = datetime.now()
        self.current_metrics.mem_used_percent = mem.percent
        self.current_metrics.mem_used_gib = bytes_to_gib(mem.used)
        self.current_metrics.mem_free_gib = bytes_to_gib(mem.free)

        swap = psutil.swap_memory()
        self.current_metrics.timestamp = datetime.now()
        self.current_metrics.swap_used_percent = swap.percent
        self.current_metrics.swap_used_gib = bytes_to_gib(swap.used)
        self.current_metrics.swap_free_gib = bytes_to_gib(swap.free)
