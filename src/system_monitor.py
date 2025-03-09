from src.config import Config
import threading
import time

from src.monitor.base import BaseMonitor
from threading import Thread
from typing import Optional


class SystemMonitor:
    def __init__(self) -> None:
        self.refresh_interval_s: float = Config().DATA_COLLECTION_INTERVAL_S
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
            time.sleep(self.refresh_interval_s)
