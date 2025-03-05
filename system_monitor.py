import time
import threading

from threading import Thread
from typing import Optional
from monitor.cpu_load_monitor import CPULoadMonitor
from monitor.memory_monitor import MemoryMonitor


class SystemMonitor:
    def __init__(self) -> None:
        self.refresh_interval_s: float = 1.0

        self._running: bool = False
        self._thread: Optional[Thread] = None
        self._cpu_monitor = CPULoadMonitor()
        self._memory_monitor = MemoryMonitor()

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

        self._cpu_monitor.start()
        self._memory_monitor.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()
        self._thread = None

    def _run(self) -> None:
        while self._running:
            print(
                f"CPU load: {self._cpu_monitor.current_metrics.usage_total:.1f}%"
                "\n"
                f"VRAM: {self._memory_monitor.current_metrics.mem_used_gib:.1f} GiB ({self._memory_monitor.current_metrics.mem_used_percent:.1f}%), {self._memory_monitor.current_metrics.mem_free_gib:.1f} GiB free"
                "\n"
                f"SWAP: {self._memory_monitor.current_metrics.swap_used_gib:.1f} GiB ({self._memory_monitor.current_metrics.swap_used_percent:.1f}%), {self._memory_monitor.current_metrics.swap_free_gib:.1f} GiB free"
                "\n"
            )

            time.sleep(self.refresh_interval_s)
