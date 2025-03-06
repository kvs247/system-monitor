import threading
import time

from abc import abstractmethod, ABC
from typing import Optional, TypeVar, Generic
from threading import Thread
from dtypes import SystemMetric

T = TypeVar("T", bound=SystemMetric, covariant=True)


class BaseMonitor(Generic[T], ABC):
    def __init__(self, collection_interval_s: float = 1.0):
        self.collection_interval_s = collection_interval_s
        self.current_metrics: T = self._init_current_metrics()

        self._running: bool = False
        self._thread: Optional[Thread] = None

    @abstractmethod
    def _init_current_metrics(self) -> T:
        pass

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
