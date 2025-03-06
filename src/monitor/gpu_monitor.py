import pynvml  # type: ignore

from datetime import datetime
from dtypes import GPUMetrics
from monitor.base import BaseMonitor
from utils import bytes_to_gib


class GPUMonitor(BaseMonitor[GPUMetrics]):
    def __init__(self) -> None:
        super().__init__()
        pynvml.nvmlInit()

        self._device_count = pynvml.nvmlDeviceGetCount()

    def _init_current_metrics(self) -> GPUMetrics:
        return GPUMetrics(
            timestamp=datetime.now(),
            memory_occupancy_percent=0.0,
            memory_used_gib=0.0,
            memory_free_gib=0.0,
            gpu_utilization_percent=0.0,
            memory_bandwidth_percent=0.0,
            temp_c=0.0,
            power_w=0.0)

    def _collect(self) -> None:
        for i in range(self._device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)

            name = pynvml.nvmlDeviceGetName(handle)
            self.current_metrics.timestamp = datetime.now()

            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            self.current_metrics.memory_used_gib = bytes_to_gib(
                float(memory_info.used))
            self.current_metrics.memory_free_gib = bytes_to_gib(
                float(memory_info.free))
            self.current_metrics.memory_occupancy_percent = float(
                memory_info.used) / float(memory_info.total) * 100

            util_rates = pynvml.nvmlDeviceGetUtilizationRates(handle)
            self.current_metrics.gpu_utilization_percent = float(
                util_rates.gpu)
            self.current_metrics.memory_bandwidth_percent = float(
                util_rates.memory)

            temp = pynvml.nvmlDeviceGetTemperature(
                handle, pynvml.NVML_TEMPERATURE_GPU)
            self.current_metrics.temp_c = float(temp)

            power = pynvml. nvmlDeviceGetPowerUsage(handle) / 1000.0  # mW to W
            self.current_metrics.power_w = float(power)
