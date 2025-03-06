import config as config
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import dataclass, fields
from dtypes import MetricsDataPoint
from matplotlib.lines import Line2D
from system_monitor import SystemMonitor
from typing import Callable


@dataclass
class Line:
    line: Line2D
    update_data: Callable[[MetricsDataPoint], float]
    label: str
    display: bool


@dataclass
class PlotLines:
    cpu_usage_total: Line
    mem_used_percent: Line


class Plotter:
    def __init__(self, data_producer: SystemMonitor) -> None:
        self._data_producer = data_producer

        self._fig, self._ax = plt.subplots()
        self._init_plot_lines()
        self._ax.set_xlim(0, config.NUM_DATA_POINTS)
        self._ax.set_ylim(0, 100)
        self._ax.grid(True)
        self._x_data = np.arange(0, config.NUM_DATA_POINTS)

        self.animation = animation.FuncAnimation(
            self._fig, self._update_data, interval=config.PLOT_INTERVAL_S, blit=True
        )

    def _init_plot_lines(self):
        self._lines = PlotLines(
            cpu_usage_total=Line(
                line=self._ax.plot([], [])[0],
                update_data=lambda x: x.cpu.usage_total,
                label="CPU Usage",
                display=True,
            ),
            mem_used_percent=Line(
                line=self._ax.plot([], [])[0],
                update_data=lambda x: x.mem.mem_used_percent,
                label="Memory Usage",
                display=True,
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

        cpu_usage_toal: list[float] = list(
            map(lambda x: x.cpu.usage_total, metrics_data))
        if len(cpu_usage_toal) < config.NUM_DATA_POINTS:
            fill_length = config.NUM_DATA_POINTS - len(cpu_usage_toal)
            cpu_usage_toal += [np.nan] * fill_length

        mem_usage_percent: list[float] = list(
            map(lambda x: x.mem.mem_used_percent, metrics_data))
        if len(mem_usage_percent) < config.NUM_DATA_POINTS:
            fill_length = config.NUM_DATA_POINTS - len(mem_usage_percent)
            mem_usage_percent += [np.nan] * fill_length

        for f in fields(self._lines):
            attr: Line = getattr(self._lines, f.name)
            data: list[float] = list(map(attr.update_data, metrics_data))
            fill_length = config.NUM_DATA_POINTS - len(data)
            data += [np.nan] * fill_length
            attr.line.set_data(self._x_data, data)

        return [getattr(self._lines, f.name).line for f in fields(self._lines)]

    def show(self) -> None:
        plt.title("System Metrics")
        self._ax.legend()
        plt.show()

    def close(self) -> None:
        plt.close(self._fig)
