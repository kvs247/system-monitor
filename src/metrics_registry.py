import src.config as config
import numpy as np

from collections import deque
from dataclasses import dataclass
from src.dtypes import Metric, HardwareComponent, MetricUnit


@dataclass
class SystemMetrics:
    # CPU
    cpu_usage_percent: Metric

    # GPU
    gpu_usage_percent: Metric
    gpu_temp_c: Metric

    # Memory
    memory_usage_percent: Metric
    memory_used_gib: Metric
    memory_free_gib: Metric
    swap_usage_gib: Metric


class MetricsRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsRegistry, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
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
                label="GPU Temp",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.CELSCIUS,
                color="blue",
                display=True,
                data=make_empty_deque(),
            ),


            # Memory
            memory_usage_percent=Metric(
                label="Memory Usage (%)",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.PERCENT,
                color="blue",
                display=True,
                data=make_empty_deque(),
            ),
            memory_used_gib=Metric(
                label="Used Memory (GiB)",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
            memory_free_gib=Metric(
                label="Free Memory (GiB)",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
            swap_usage_gib=Metric(
                label="Swap Usage",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                color="red",
                display=True,
                data=make_empty_deque(),
            ),
        )

    def get_system_metrics(self) -> SystemMetrics:
        return self._system_metrics
