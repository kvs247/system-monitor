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

            # name = pynvml.nvmlDeviceGetName(handle)
            # self.current_metrics.timestamp = datetime.now()

            # memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            # self.current_metrics.memory_used_gib = bytes_to_gib(
            #     float(memory_info.used))
            # self.current_metrics.memory_free_gib = bytes_to_gib(
            #     float(memory_info.free))
            # self.current_metrics.memory_occupancy_percent = float(
            #     memory_info.used) / float(memory_info.total) * 100

            util_rates = pynvml.nvmlDeviceGetUtilizationRates(handle)
            # self.current_metrics.gpu_utilization_percent = float(
            #     util_rates.gpu)
            # self.current_metrics.memory_bandwidth_percent = float(
            #     util_rates.memory)

            temp = pynvml.nvmlDeviceGetTemperature(
                handle, pynvml.NVML_TEMPERATURE_GPU)
            self.system_metrics.gpu_temp_c.update(float(temp))

            # power = pynvml. nvmlDeviceGetPowerUsage(handle) / 1000.0  # mW to W
            # self.current_metrics.power_w = float(power)

            self.system_metrics.gpu_usage_percent.update(float(util_rates.gpu))
