import src.config as config
import numpy as np

from collections import deque
from dataclasses import dataclass
from src.dtypes import Metric, HardwareComponent, MetricUnit


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


class MetricsRegistry:
    _instance = None

    def __new__(cls) -> "MetricsRegistry":
        if cls._instance is None:
            cls._instance = super(MetricsRegistry, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        def make_empty_deque() -> deque[float]:
            return deque([np.nan] * config.NUM_DATA_POINTS, maxlen=config.NUM_DATA_POINTS)

        self._system_metrics = SystemMetrics(
            # CPU
            cpu_usage_percent=Metric(
                label="CPU Utilization",
                hardware_component=HardwareComponent.CPU,
                unit=MetricUnit.PERCENT,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
            cpu_temp_avg_c=Metric(
                label="Average CPU Temperature",
                hardware_component=HardwareComponent.CPU,
                unit=MetricUnit.CELSCIUS,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
            cpu_temp_max_c=Metric(
                label="Maximum CPU Temperature",
                hardware_component=HardwareComponent.CPU,
                unit=MetricUnit.CELSCIUS,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),

            # GPU
            gpu_usage_percent=Metric(
                label="GPU Utilization",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.PERCENT,
                color="yellow",
                display=True,
                data=make_empty_deque(),
            ),
            gpu_temp_c=Metric(
                label="GPU Temperature",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.CELSCIUS,
                color="blue",
                display=True,
                data=make_empty_deque(),
            ),
            gpu_memory_usage_percent=Metric(
                label="GPU Memory Utilization",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.PERCENT,
                color="blue",
                display=True,
                data=make_empty_deque(),
            ),
            gpu_memory_bandwidth=Metric(
                label="GPU Memory Bandwidth",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.PERCENT,
                color="",
                display=True,
                data=make_empty_deque(),
            ),
            gpu_memory_used_gib=Metric(
                label="Used GPU Memory",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.GIB,
                color="blue",
                display=True,
                data=make_empty_deque(),
            ),
            gpu_memory_free_gib=Metric(
                label="Free GPU Memory",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.GIB,
                color="blue",
                display=True,
                data=make_empty_deque(),
            ),


            # Memory
            memory_usage_percent=Metric(
                label="Memory Usage",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.PERCENT,
                color="blue",
                display=True,
                data=make_empty_deque(),
            ),
            memory_used_gib=Metric(
                label="Used Memory",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
            memory_free_gib=Metric(
                label="Free Memory",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
            swap_usage_percent=Metric(
                label="Swap Utiliazation",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.PERCENT,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
            swap_used_gib=Metric(
                label="Used Swap",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
            swap_free_gib=Metric(
                label="Free Swap",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
        )

    def get_system_metrics(self) -> SystemMetrics:
        return self._system_metrics
