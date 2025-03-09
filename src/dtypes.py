from collections import deque
from dataclasses import dataclass
from enum import Enum, auto


class HardwareComponent(Enum):
    CPU = "cpu"
    GPU = "gpu"
    MEMORY = "memory"


class MetricUnit(Enum):
    PERCENT = auto()
    GIB = auto()
    CELSCIUS = auto()


@dataclass
class MetricConfig:
    color: str
    display: bool


@dataclass
class Metric:
    label: str
    hardware_component: HardwareComponent
    unit: MetricUnit
    config: MetricConfig
    data: deque[float]

    def update(self, value: float) -> None:
        self.data.append(value)


@dataclass
class SystemMetrics:
    # CPU
    cpu_usage_percent: Metric
    cpu_temp_avg_c: Metric
    cpu_temp_max_c: Metric

    # GPU
    gpu_usage_percent: Metric
    gpu_temp_c: Metric
    gpu_memory_usage_percent: Metric
    gpu_memory_bandwidth: Metric
    gpu_memory_used_gib: Metric
    gpu_memory_free_gib: Metric

    # Memory
    memory_usage_percent: Metric
    memory_used_gib: Metric
    memory_free_gib: Metric
    swap_usage_percent: Metric
    swap_used_gib: Metric
    swap_free_gib: Metric
