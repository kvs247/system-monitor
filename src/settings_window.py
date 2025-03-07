import tkinter as tk

from dtypes import PlotLines


class SettingsWindow:
    def __init__(self, plot_lines: PlotLines):
        self._root = tk.Tk()
        self._root.title("Settings")
        self._root.minsize(200, 200)
        self._root.geometry("300x300+50+50")
        self._root.configure(background="black")

        self._hidden = False
        self._plot_lines = plot_lines

    def is_hidden(self) -> bool:
        return self._hidden

    def show(self) -> None:
        self._hidden = False
        self._root.deiconify()
        self._root.update()

    def hide(self) -> None:
        self._hidden = True
        self._root.withdraw()
