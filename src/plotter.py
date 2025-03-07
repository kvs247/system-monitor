import config
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import fields
from dtypes import PlotLines, Line
from matplotlib.backend_bases import Event
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
from settings_window import SettingsWindow
from system_monitor import SystemMonitor
from typing import Optional


class Plotter:
    def __init__(self, data_producer: SystemMonitor) -> None:
        self._data_producer = data_producer

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
        self._lines = PlotLines(
            cpu_usage_total=Line(
                line=self._ax.plot([], [])[0],
                update_data=lambda x: x.cpu.usage_total_percent,
                label="CPU Usage",
                display=True,
            ),
            mem_used_percent=Line(
                line=self._ax.plot([], [])[0],
                update_data=lambda x: x.memory.memory_used_percent,
                label="Memory Usage",
                display=True,
            ),
            gpu_utilization=Line(
                line=self._ax.plot([], [])[0],
                update_data=lambda x: x.gpu.gpu_utilization_percent,
                label="GPU Utilization",
                display=True
            ),
        )
        self._set_line_labels()

    def _set_line_labels(self):
        for f in fields(self._lines):
            attr: Line = getattr(self._lines, f.name)
            attr.line.set_label(attr.label)

    def _update_data(self, _: None) -> list[Line2D]:
        metrics_data = self._data_producer.get_metrics_data()
        if not metrics_data:
            return [getattr(self._lines, f.name).line for f in fields(self._lines)]

        for f in fields(self._lines):
            attr: Line = getattr(self._lines, f.name)
            data: list[float] = list(map(attr.update_data, metrics_data))
            fill_length = config.NUM_DATA_POINTS - len(data)
            data += [np.nan] * fill_length
            attr.line.set_data(self._x_data, data)

        return [getattr(self._lines, f.name).line for f in fields(self._lines)]

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
        self._ax.legend()
        plt.show()

    def close(self) -> None:
        plt.close(self._fig)
