import config
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from system_monitor import SystemMonitor
from matplotlib.lines import Line2D


class Plotter:
    def __init__(self, data_producer: SystemMonitor) -> None:
        self._data_producer = data_producer

        self._fig, self._ax = plt.subplots()
        self._line, = self._ax.plot([], [])
        self._ax.set_xlim(0, config.NUM_DATA_POINTS)
        self._ax.set_ylim(0, 100)
        self._ax.grid(True)
        self._x_data = np.arange(0, config.NUM_DATA_POINTS)

        self.animation = animation.FuncAnimation(
            self._fig, self._update_data, interval=config.PLOT_INTERVAL_S, blit=True
        )

    def _update_data(self, _: None) -> list[Line2D]:
        metrics_data = self._data_producer.get_metrics_data()
        if not metrics_data:
            return [self._line]

        cpu_usage_toal: list[float] = list(
            map(lambda x: x.cpu.usage_total, metrics_data))
        if len(cpu_usage_toal) < config.NUM_DATA_POINTS:
            fill_length = config.NUM_DATA_POINTS - len(cpu_usage_toal)
            cpu_usage_toal += [np.nan] * fill_length

        x_data = np.arange(0, config.NUM_DATA_POINTS)
        self._line.set_data(x_data, cpu_usage_toal)

        return [self._line]

    def show(self) -> None:
        plt.title("System Metrics")
        plt.show()

    def close(self) -> None:
        plt.close(self._fig)
