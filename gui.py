"""Graphic interface of the app"""
import tkinter as tk
from tkinter import ttk
from game import Game
from record_manager import RecordManager


class Gui:
    """GUI Class"""

    def __init__(self):

        self.record_manager = RecordManager()

        background_color = "gray22"
        font_color = "white"

        self.ventana = tk.Tk()
        self.ventana.title("Minesweeper")
        self.ventana.config(bg=background_color)
        self.ventana.geometry("300x200")
        self.ventana.resizable(False, False)

        self.ventana.wait_visibility()
        Game.aling_center_root(self.ventana)

        self.title = tk.Label(
            self.ventana, text="Minesweeper", font=("Arial", 20), bg=background_color,
            fg=font_color)
        self.title.pack(pady=25, padx=20)

        self.difficulties = ["Easy", "Medium", "Hard"]
        self.combobox = ttk.Combobox(
            self.ventana, values=self.difficulties, state="readonly")
        self.combobox.set(self.difficulties[1])
        self.combobox.pack(pady=5)
        self.combobox.bind("<<ComboboxSelected>>",
                           lambda x: self.show_record(self.combobox.get()))

        self.record_label = tk.Label(
            self.ventana, fg="lightgray", bg="gray22", font="Arial 8 italic", anchor="w")
        self.record_label.pack()
        self.show_record("Medium")

        self.play_button = tk.Button(
            self.ventana,  text="Play", width=8, command=self.play)
        self.play_button.pack(pady=15)

    def play(self):
        """Instantiate game"""
        option = self.combobox.get()
        if option in self.difficulties:
            self.ventana.destroy()
            g = Game(option)
            g.start()

    def show_record(self, difficulty):
        """Show the record with the difficulty"""
        record = int(self.record_manager.get_record_in_difficulty(difficulty))
        if record == 0:
            formated = "--:--"
        else:
            formated = Game.seconds_to_minutes_seconds(record)
        self.record_label.config(
            text="record: " + formated)

    def start(self):
        """Start the app"""
        self.ventana.mainloop()
