import threading
import time

from abc import abstractmethod, ABC
from src.metrics_registry.metrics_registry import MetricsRegistry
from threading import Thread
from typing import Optional


class BaseMonitor(ABC):
    def __init__(self, collection_interval_s: float = 1.0):
        self.collection_interval_s = collection_interval_s
        self.system_metrics = MetricsRegistry().get_system_metrics()

        self._running: bool = False
        self._thread: Optional[Thread] = None

    def _collection_loop(self) -> None:
        while self._running:
            start_time = time.time()
            self._collect()

            elapsed_time = time.time() - start_time
            if (elapsed_time < self.collection_interval_s):
                time.sleep(self.collection_interval_s - elapsed_time)

    @abstractmethod
    def _collect(self) -> None:
        pass

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._collection_loop)
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()
        self._thread = None
