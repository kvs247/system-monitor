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
class Metric:
    label: str
    hardware_component: HardwareComponent
    unit: MetricUnit
    color: str
    display: bool
    data: deque[float]

    def update(self, value: float) -> None:
        self.data.append(value)
