import src.config as config
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import fields
from matplotlib.backend_bases import Event
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
from src.dtypes import Metric
from src.metrics_registry import MetricsRegistry
from src.visualization.settings_window import SettingsWindow
from src.system_monitor import SystemMonitor
from typing import Optional


class Plotter:
    def __init__(self, data_producer: SystemMonitor) -> None:
        self._data_producer = data_producer
        self._registry = MetricsRegistry()

        self._fig, self._ax = plt.subplots()
        self._init_plot_lines()
        self._ax.set_xlim(0, config.NUM_DATA_POINTS)
        self._ax.set_ylim(0, 100)
        self._ax.grid(True)
        self._x_data = np.arange(0, config.NUM_DATA_POINTS)

        self._settings_window: Optional[SettingsWindow] = None
        self._add_settings_button()

        self.animation = animation.FuncAnimation(
            self._fig, self._update_data, interval=config.PLOT_INTERVAL_S, blit=True
        )

    def _init_plot_lines(self):
        self._lines: list[Line2D] = []
        for f in fields(self._registry.get_system_metrics()):
            self._lines.append(self._ax.plot([], [])[0])

    def _update_data(self, _: None) -> list[Line2D]:
        system_metrics = self._registry.get_system_metrics()
        i: int = 0
        for f in fields(system_metrics):
            attr: Metric = getattr(system_metrics, f.name)
            if attr.display:
                data = attr.data
                fill_length = config.NUM_DATA_POINTS - len(data)
                data += [np.nan] * fill_length
                self._lines[i].set_data(self._x_data, data)
            else:
                self._lines[i].set_data([], [])
            i += 1

        return self._lines

    def _get_labels(self) -> list[str]:
        labels: list[str] = []
        for f in fields(self._registry.get_system_metrics()):
            attr: Metric = getattr(self._registry.get_system_metrics(), f.name)
            labels.append(attr.label)
        return labels

    def _add_settings_button(self):
        settings_ax = plt.axes((0.85, 0.01, 0.1, 0.05))
        self._settings_button = Button(settings_ax, "Settings")
        self._settings_button.on_clicked(self._handle_click_settings)

    def _handle_click_settings(self, _: Event):
        if self._settings_window is None:
            self._settings_window = SettingsWindow(self._lines)
            self._settings_window.show()
        elif self._settings_window.is_hidden():
            self._settings_window.show()
        else:
            self._settings_window.hide()

    def show(self) -> None:
        plt.title("System Metrics")
        self._ax.legend(self._get_labels())
        plt.show()

    def close(self) -> None:
        plt.close(self._fig)
