import os
import json

from typing import Any, Optional, Dict
from dataclasses import fields, asdict
from src.dtypes import Metric, MetricConfig, SystemMetrics

HOME = os.path.expanduser("~")
SYSTEM_MONITOR_DIR = os.path.join(HOME, ".config/system-monitor")
CONFIG_FILE_PATH_UNIX = os.path.join(SYSTEM_MONITOR_DIR, "settings.json")


class Config:
    _instance = None

    NUM_DATA_POINTS: int = 600
    PLOT_INTERVAL_S: float = 1.0
    DATA_COLLECTION_INTERVAL_S: float = 1.0

    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
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

    def write_config_file(self, system_metrics: SystemMetrics) -> None:
        if not self._config_dir_exists():
            self._create_config_dir()

        config_file_json: Dict[str, Dict[str, Any]] = {}
        for f in fields(system_metrics):
            metric: Metric = getattr(system_metrics, f.name)
            config_file_json[f.name] = asdict(metric.config)

        with open(CONFIG_FILE_PATH_UNIX, "w") as f:
            f.write(json.dumps(config_file_json, indent=2))

    def read_config_file(self) -> Optional[Dict[str, MetricConfig]]:
        if not self._config_file_exists():
            return None

        config_file_json: Dict[str, Any] = {}
        with open(CONFIG_FILE_PATH_UNIX, "r") as f:
            config_file_json = json.loads(f.read())

        if len(config_file_json) == 0:
            return None

        config_data: Dict[str, MetricConfig] = {}
        for metric_name, metric_config in config_file_json.items():
            config_data[metric_name] = MetricConfig(color=metric_config["color"], display=metric_config["display"])

        return config_data
