import time
import threading

from threading import Thread
from typing import Optional
from monitor.cpu_load_monitor import CPULoadMonitor


class SystemMonitor:
    def __init__(self) -> None:
        self.refresh_interval_s: float = 1.0

        self._running: bool = False
        self._thread: Optional[Thread] = None
        self._cpu_monitor = CPULoadMonitor()

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

        self._cpu_monitor.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()
        self._thread = None

    def _run(self) -> None:
        while self._running:
            print(
                f"CPU usage: {self._cpu_monitor.current_metrics.usage_total}%")

            time.sleep(self.refresh_interval_s)
