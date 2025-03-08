import pynvml  # type: ignore

from src.monitor.base import BaseMonitor
from utils import bytes_to_gib


class GPUMonitor(BaseMonitor):
    def __init__(self) -> None:
        super().__init__()
        pynvml.nvmlInit()

        self._device_count = pynvml.nvmlDeviceGetCount()

    def _collect(self) -> None:
        for i in range(self._device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)

            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            self.system_metrics.gpu_memory_used_gib.update(
                bytes_to_gib(float(memory_info.used)))
            self.system_metrics.gpu_memory_free_gib.update(
                bytes_to_gib(float(memory_info.free)))
            self.system_metrics.gpu_memory_usage_percent.update(
                float(memory_info.used) / float(memory_info.total) * 100)
            self.system_metrics.gpu_memory_usage_percent

            util_rates = pynvml.nvmlDeviceGetUtilizationRates(handle)
            self.system_metrics.gpu_usage_percent.update(float(util_rates.gpu))
            self.system_metrics.gpu_memory_bandwidth.update(
                float(util_rates.memory))

            temp = pynvml.nvmlDeviceGetTemperature(
                handle, pynvml.NVML_TEMPERATURE_GPU)
            self.system_metrics.gpu_temp_c.update(float(temp))
