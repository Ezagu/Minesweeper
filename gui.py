"""Graphic interface of the app"""
import tkinter as tk
from tkinter import ttk
from game import Game


class Gui:
    """GUI Class"""

    def __init__(self):

        background_color = "gray22"
        font_color = "white"

        self.ventana = tk.Tk()
        self.ventana.title("Minesweeper")
        self.ventana.config(bg=background_color)
        self.ventana.geometry("300x200")
        self.ventana.resizable(False, False)

        self.title = tk.Label(
            self.ventana, text="Minesweeper", font=("Arial", 20), bg=background_color, fg=font_color)
        self.title.pack(pady=25, padx=20)

        self.difficulties = ["Easy", "Medium", "Hard"]
        self.combobox = ttk.Combobox(
            self.ventana, values=self.difficulties, state="readonly")
        self.combobox.set(self.difficulties[1])
        self.combobox.pack(pady=10)

        self.play_button = tk.Button(
            self.ventana,  text="Play", width=8, command=self.play)
        self.play_button.pack(pady=10)

    def play(self):
        """Instantiate game"""
        option = self.combobox.get()
        if option in self.difficulties:
            self.ventana.destroy()
            g = Game(option)
            g.start()

    def start(self):
        """Start the app"""
        self.ventana.mainloop()
