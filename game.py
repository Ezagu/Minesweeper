"""Instantiate a window with the game"""
import tkinter as tk


class Game:
    """Game class"""

    def __init__(self, option: str):
        """option -> difficulty"""
        self.ventana = tk.Tk()

    def start(self):
        """Start the window"""
        self.ventana.mainloop()
