"""Graphic interface of the app"""
import tkinter as tk


class Gui:
    """GUI Class"""

    def __init__(self):
        self.ventana = tk.Tk()

    def iniciar(self):
        """Start the app"""
        self.ventana.mainloop()
