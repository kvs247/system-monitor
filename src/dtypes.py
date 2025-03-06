from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class CPULoadMetrics:
    timestamp: datetime
    usage_total: float
    usage_percpu: list[float]


@dataclass
class MemoryMetrics:
    timestamp: datetime
    mem_used_percent: float
    mem_used_gib: float
    mem_free_gib: float
    swap_used_percent: float
    swap_used_gib: float
    swap_free_gib: float


@dataclass(frozen=True)
class MetricsDataPoint:
    cpu: CPULoadMetrics
    mem: MemoryMetrics


SystemMetric = Union[CPULoadMetrics, MemoryMetrics]
