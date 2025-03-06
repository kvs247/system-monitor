from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class CPULoadMetrics:
    timestamp: datetime
    usage_total_percent: float
    usage_percpu_percent: list[float]


@dataclass
class MemoryMetrics:
    timestamp: datetime
    memory_used_percent: float
    memory_used_gib: float
    memory_free_gib: float
    swap_used_percent: float
    swap_used_gib: float
    swap_free_gib: float


@dataclass
class GPUMetrics:
    timestamp: datetime
    memory_occupancy_percent: float
    memory_used_gib: float
    memory_free_gib: float
    gpu_utilization_percent: float
    memory_bandwidth_percent: float
    temp_c: float
    power_w: float


@dataclass(frozen=True)
class MetricsDataPoint:
    cpu: CPULoadMetrics
    memory: MemoryMetrics
    gpu: GPUMetrics


SystemMetric = Union[CPULoadMetrics, MemoryMetrics, GPUMetrics]
