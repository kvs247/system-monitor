import tkinter as tk

from dataclasses import fields
from matplotlib.lines import Line2D
from src.dtypes import Metric
from src.metrics_registry import MetricsRegistry


class SettingsWindow:
    def __init__(self, plot_lines: list[Line2D]):
        self._root = tk.Tk()
        self._root.title("Settings")
        self._root.minsize(200, 200)
        self._root.geometry("300x300+50+50")
        self._root.configure(background="black")

        self._hidden = False
        self._plot_lines = plot_lines
        self._metrics_registry = MetricsRegistry()
        self._system_metrics = self._metrics_registry.get_system_metrics()

        for f in fields(self._system_metrics):
            attr: Metric = getattr(
                self._system_metrics, f.name)
            check_button = tk.Checkbutton(
                self._root,
                text=f.name,
                command=lambda a=attr: self.change_field_active(a),
            )
            check_button.pack()

            if attr.display:
                check_button.select()
            else:
                check_button.deselect()

    def is_hidden(self) -> bool:
        return self._hidden

    def show(self) -> None:
        self._hidden = False
        self._root.deiconify()
        self._root.update()

    def hide(self) -> None:
        self._hidden = True
        self._root.withdraw()

    def change_field_active(self, attr: Metric) -> None:
        attr.display = not attr.display
