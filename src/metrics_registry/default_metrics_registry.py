from src.config import Config
import numpy as np

from collections import deque
from src.dtypes import Metric, MetricConfig, MetricUnit, HardwareComponent, SystemMetrics


def make_empty_deque() -> deque[float]:
    return deque([np.nan] * Config().NUM_DATA_POINTS, maxlen=Config().NUM_DATA_POINTS)


def make_default_metrics_registry() -> SystemMetrics:
    return (
        SystemMetrics(
            # CPU
            cpu_usage_percent=Metric(
                label="CPU Utilization",
                hardware_component=HardwareComponent.CPU,
                unit=MetricUnit.PERCENT,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            cpu_temp_avg_c=Metric(
                label="Average CPU Temperature",
                hardware_component=HardwareComponent.CPU,
                unit=MetricUnit.CELSCIUS,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            cpu_temp_max_c=Metric(
                label="Maximum CPU Temperature",
                hardware_component=HardwareComponent.CPU,
                unit=MetricUnit.CELSCIUS,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),

            # GPU
            gpu_usage_percent=Metric(
                label="GPU Utilization",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.PERCENT,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            gpu_temp_c=Metric(
                label="GPU Temperature",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.CELSCIUS,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            gpu_memory_usage_percent=Metric(
                label="GPU Memory Utilization",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.PERCENT,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            gpu_memory_bandwidth=Metric(
                label="GPU Memory Bandwidth",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.PERCENT,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            gpu_memory_used_gib=Metric(
                label="Used GPU Memory",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.GIB,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            gpu_memory_free_gib=Metric(
                label="Free GPU Memory",
                hardware_component=HardwareComponent.GPU,
                unit=MetricUnit.GIB,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),


            # Memory
            memory_usage_percent=Metric(
                label="Memory Usage",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.PERCENT,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            memory_used_gib=Metric(
                label="Used Memory",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            memory_free_gib=Metric(
                label="Free Memory",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            swap_usage_percent=Metric(
                label="Swap Utiliazation",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.PERCENT,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            swap_used_gib=Metric(
                label="Used Swap",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
            swap_free_gib=Metric(
                label="Free Swap",
                hardware_component=HardwareComponent.MEMORY,
                unit=MetricUnit.GIB,
                config=MetricConfig(color="red", display=True),
                data=make_empty_deque(),
            ),
        )
    )
