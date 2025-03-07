import tkinter as tk

from dtypes import PlotLines, Line
from dataclasses import fields


class SettingsWindow:
    def __init__(self, plot_lines: PlotLines):
        self._root = tk.Tk()
        self._root.title("Settings")
        self._root.minsize(200, 200)
        self._root.geometry("300x300+50+50")
        self._root.configure(background="black")

        self._hidden = False
        self._plot_lines = plot_lines

        for f in fields(plot_lines):
            attr: Line = getattr(plot_lines, f.name)
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

    def change_field_active(self, attr: Line) -> None:
        attr.display = not attr.display
