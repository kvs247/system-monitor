# pyright: reportUnknownMemberType=false

from src.config import Config
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import fields
from matplotlib.axes import Axes
from matplotlib.backend_bases import Event
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
from PIL import Image
from src.dtypes import Metric, MetricUnit
from src.metrics_registry.metrics_registry import MetricsRegistry
from src.system_monitor import SystemMonitor
from src.utils import get_metric_unit_ylim, get_metric_unit_label
from src.visualization.settings_window import SettingsWindow
from typing import Optional, Tuple

BACKGROUND_COLOR = "#333333"
WHITE = "#DDDDDD"
GEAR_ICON_PATH = "assets/gear.png"


def make_xticks(num_ticks: int) -> Tuple[list[float], list[str]]:
    ticks = list(np.linspace(0, Config().NUM_DATA_POINTS, num_ticks).astype(float))
    labels = [str(int((Config().NUM_DATA_POINTS - t)) * Config().INTERVAL_S) for t in ticks]

    return ticks, labels


class Plotter:
    def __init__(self, data_producer: SystemMonitor) -> None:
        self._data_producer = data_producer
        self._registry = MetricsRegistry()
        self._num_unit_types = len(MetricUnit)

        self._fig: Figure
        self._axes: list[Axes]
        self._fig, self._axes = plt.subplots(self._num_unit_types, 1)
        self._fig.set_facecolor(BACKGROUND_COLOR)

        self._init_plot_lines()

        for i in range(self._num_unit_types):
            self._axes[i].set_facecolor(BACKGROUND_COLOR)
            self._axes[i].set_xlim(0, Config().NUM_DATA_POINTS)
            self._axes[i].set_ylim(0, get_metric_unit_ylim(MetricUnit(i + 1)))
            self._axes[i].grid(axis="y", color=WHITE, zorder=0, alpha=0.5)
            self._axes[i].tick_params(axis="both", colors=WHITE)
            self._axes[i].set_ylabel(
                get_metric_unit_label(MetricUnit(i + 1)),
                color=WHITE,
                rotation=0,
                labelpad=10
            )

            if i == self._num_unit_types - 1:
                self._axes[i].set_xlabel("s", color=WHITE)
                self._axes[i].set_xticks(*make_xticks(11))
            else:
                self._axes[i].set_xticks([])

            for spine in self._axes[i].spines.values():
                spine.set_color(WHITE)
                spine.set_zorder(0)

        self._x_data = np.arange(0, Config().NUM_DATA_POINTS)

        self._settings_window: Optional[SettingsWindow] = None
        self._add_settings_button()

        self.animation = animation.FuncAnimation(
            self._fig, self._update_data, interval=Config().INTERVAL_S, blit=True
        )

    def _init_plot_lines(self) -> None:
        self._lines: list[Line2D] = []
        for f in fields(self._registry.get_system_metrics()):
            attr: Metric = getattr(self._registry.get_system_metrics(), f.name)
            plot_index = attr.unit.value - 1
            self._lines.append(self._axes[plot_index].plot([], [])[0])

    def _update_data(self, _: None) -> list[Line2D]:
        system_metrics = self._registry.get_system_metrics()
        i: int = 0
        for f in fields(system_metrics):
            attr: Metric = getattr(system_metrics, f.name)
            if attr.config.display:
                data = attr.data
                fill_length = Config().NUM_DATA_POINTS - len(data)
                data += [np.nan] * fill_length
                self._lines[i].set_data(self._x_data, data)
            else:
                self._lines[i].set_data([], [])
            i += 1

        return self._lines

    def _get_labels(self) -> list[list[str]]:
        labels: list[list[str]] = [[] for _ in range(self._num_unit_types)]
        for f in fields(self._registry.get_system_metrics()):
            attr: Metric = getattr(self._registry.get_system_metrics(), f.name)
            unit_index = attr.unit.value - 1
            labels[unit_index].append(attr.label)
        return labels

    def _add_settings_button(self) -> None:
        settings_ax = plt.axes((0.9625, 0.95, 0.05, 0.05))
        gear_img = Image.open(GEAR_ICON_PATH)

        settings_ax.set_facecolor("none")
        settings_ax.patch.set_visible(False)

        self._settings_button = Button(
            settings_ax,
            label="",
            image=gear_img,
        )

        self._settings_button.on_clicked(self._handle_click_settings)

    def _handle_click_settings(self, _: Event) -> None:
        if self._settings_window is None:
            self._settings_window = SettingsWindow(self._lines)
            self._settings_window.show()
        elif self._settings_window.is_hidden():
            self._settings_window.show()
        else:
            self._settings_window.hide()

    def show(self) -> None:
        labels = self._get_labels()
        for i in range(self._num_unit_types):
            self._axes[i].legend(labels[i], loc="upper left")
        plt.tight_layout()
        plt.show()

    def close(self) -> None:
        plt.close(self._fig)
