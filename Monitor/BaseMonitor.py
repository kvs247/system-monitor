import threading
import time

from typing import Optional
from threading import Thread


class BaseMonitor:
    def __init__(self):
        self.collection_interval_s: float = 1.0

        self._running: bool = False
        self._thread: Optional[Thread] = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._collection_loop)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        self._thread = None

    def _collection_loop(self):
        while self._running:
            start_time = time.time()
            self._collect()

            elapsed_time = time.time() - start_time
            if (elapsed_time < self.collection_interval_s):
                time.sleep(self.collection_interval_s - elapsed_time)

    def _collect(self):
        """Collect metrics and update internally"""
        raise NotImplementedError("_collect() method not implemented")
