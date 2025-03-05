import time
import threading

from threading import Thread
from typing import Optional
from monitor.base import BaseMonitor


class SystemMonitor:
    def __init__(self) -> None:
        self.refresh_interval_s: float = 1.0
        self._running: bool = False
        self._thread: Optional[Thread] = None
        self._monitors: list[BaseMonitor] = []

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

    def add_monitor(self, monitor: BaseMonitor) -> None:
        self._monitors.append(monitor)

    def _init_monitors(self) -> None:
        for m in self._monitors:
            m.start()

    def _run(self) -> None:
        while self._running:
            text_width = 6
            cpu_monitor = self._monitors[0]
            mem_monitor = self._monitors[1]
            print(
                f"{'CPU: ':{text_width}}{cpu_monitor.current_metrics.usage_total:.1f}%\n"

                f"{'RAM: ':{text_width}}{mem_monitor.current_metrics.mem_used_gib:.1f} GiB "
                f"({mem_monitor.current_metrics.mem_used_percent:.1f}%), "
                f"{mem_monitor.current_metrics.mem_free_gib:.1f} GiB free\n"

                f"{'SWAP: ':{text_width}}{mem_monitor.current_metrics.swap_used_gib:.1f} GiB "
                f"({mem_monitor.current_metrics.swap_used_percent:.1f}%), "
                f"{mem_monitor.current_metrics.swap_free_gib:.1f} GiB free\n"
            )

            time.sleep(self.refresh_interval_s)
