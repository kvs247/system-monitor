import config as config
import copy
import threading
import time

from collections import deque
from dtypes import SystemMetric, MetricsDataPoint, CPULoadMetrics, MemoryMetrics, GPUMetrics
from monitor.base import BaseMonitor
from threading import Thread
from typing import Optional


class SystemMonitor:
    def __init__(self) -> None:
        self.refresh_interval_s: float = config.DATA_COLLECTION_INTERVAL_S
        self._running: bool = False
        self._thread: Optional[Thread] = None
        self._monitors: list[BaseMonitor[SystemMetric]] = []
        self._metrics_data: deque[MetricsDataPoint] = deque(
            maxlen=config.NUM_DATA_POINTS)

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()
        self._init_monitors()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()
        self._thread = None

    def add_monitor(self, monitor: BaseMonitor[SystemMetric]) -> None:
        self._monitors.append(monitor)

    def get_metrics_data(self) -> deque[MetricsDataPoint]:
        return self._metrics_data

    def _init_monitors(self) -> None:
        for m in self._monitors:
            m.start()

    def _run(self) -> None:
        while self._running:
            text_width = 6

            cpu_monitor: CPULoadMetrics = self._monitors[0].current_metrics  # type: ignore # nopep8
            mem_monitor: MemoryMetrics = self._monitors[1].current_metrics  # type: ignore # nopep8
            gpu_monitor: GPUMetrics = self._monitors[2].current_metrics  # type: ignore # nopep8
            # print(
            #     f"{'CPU: ':{text_width}}{cpu_monitor.usage_total_percent:.1f}%\n"

            #     f"{'RAM: ':{text_width}}{mem_monitor.memory_used_gib:.1f} GiB "
            #     f"({mem_monitor.memory_used_percent:.1f}%), "
            #     f"{mem_monitor.memory_free_gib:.1f} GiB free\n"

            #     f"{'SWAP: ':{text_width}}{mem_monitor.swap_used_gib:.1f} GiB "
            #     f"({mem_monitor.swap_used_percent:.1f}%), "
            #     f"{mem_monitor.swap_free_gib:.1f} GiB free\n"

            #     f"{'GPU: ':{text_width}}{gpu_monitor.memory_occupancy_percent}"
            # )

            data_point = MetricsDataPoint(
                cpu=cpu_monitor,
                memory=mem_monitor,
                gpu=gpu_monitor,
            )
            # i dont like that i have to deepcopy here
            self._metrics_data.append(copy.deepcopy(data_point))

            time.sleep(self.refresh_interval_s)
