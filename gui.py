import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import matplotlib.pyplot as plt


class QuizApp(tk.Tk):
    DARK = True

    def __init__(self):
        super().__init__()
        self.title("Quizzo")
        self.geometry("1200x700")
        self.resizable(False, False)

    def set_theme(self):
        self.style = Style(theme="darkly" if self.DARK else "cosmo")
        # ttk.Style(self.style)
        # ttk.Style.configure(self, self.style)

    def _header(self):
        header = ttk.Label(self, text="Quizzo", font=("Tahoma", 24, "bold"),
                           justify="center", style="warning.TLabel",  padding=(20, 5))
        header.pack(side="top")
        sep1 = ttk.Separator(self, orient="horizontal", style="warning.Horizontal.TSeparator")
        sep1.pack(side="top", fill="x")

    def _run_inner_funcs(self):
        self._header()

    def run(self):
        self._run_inner_funcs()
        self.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.set_theme()
    app.run()
