import os
import json

from typing import Any, Optional, Dict
from src.metrics_registry.metrics_registry import MetricsRegistry
from dataclasses import fields, asdict
from src.dtypes import Metric, MetricConfig

HOME = os.path.expanduser("~")
SYSTEM_MONITOR_DIR = os.path.join(HOME, ".config/system-monitor")
CONFIG_FILE_PATH_UNIX = os.path.join(SYSTEM_MONITOR_DIR, "settings.json")


class Settings:
    _instance = None
    config: Optional[object] = None

    def __new__(cls) -> "Settings":
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        if not os.path.exists(CONFIG_FILE_PATH_UNIX):
            print("does not exist")
        pass

    def _config_dir_exists(self) -> bool:
        return os.path.exists(SYSTEM_MONITOR_DIR)

    def _config_file_exists(self) -> bool:
        return os.path.exists(CONFIG_FILE_PATH_UNIX)

    def _create_config_dir(self) -> None:
        os.mkdir(SYSTEM_MONITOR_DIR)
        if not self._config_dir_exists():
            raise Exception(f"Error: failed to create {SYSTEM_MONITOR_DIR}")

    def write_config_file(self) -> None:
        if not self._config_dir_exists():
            self._create_config_dir()

        system_metrics = MetricsRegistry().get_system_metrics()
        config_file_json: Dict[str, Dict[str, Any]] = {}
        for f in fields(system_metrics):
            metric: Metric = getattr(system_metrics, f.name)
            config_file_json[f.name] = asdict(metric.config)

        with open(CONFIG_FILE_PATH_UNIX, "w") as f:
            f.write(json.dumps(config_file_json, indent=2))

    def load_config_file(self) -> bool:
        if not self._config_file_exists():
            return False

        config_file_json = {}
        with open(CONFIG_FILE_PATH_UNIX, "r") as f:
            config_file_json = json.loads(f.read())

        if len(config_file_json) == 0:
            return False

        system_metrics = MetricsRegistry().get_system_metrics()
        for metric_name, metric_config in config_file_json.items():
            metric: Metric = getattr(system_metrics, metric_name)
            new_metric_config = MetricConfig(color=metric_config["color"], display=metric_config["display"])
            setattr(metric, "config", new_metric_config)

        return True
