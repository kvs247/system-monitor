from src.dtypes import SystemMetrics
from src.metrics_registry.default_metrics_registry import make_default_metrics_registry


class MetricsRegistry:
    _instance = None

    def __new__(cls) -> "MetricsRegistry":
        if cls._instance is None:
            cls._instance = super(MetricsRegistry, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        self._system_metrics = make_default_metrics_registry()

    def get_system_metrics(self) -> SystemMetrics:
        return self._system_metrics
