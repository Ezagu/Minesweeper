"""Instantiate a window with the game"""
import tkinter as tk
from box import Box
from box_conteiner import BoxConteiner


class Game:
    """Game class"""

    def __init__(self, option: str):
        """option -> difficulty"""

        difficulty_settings = {"Easy": {"size": 10, "mines": 10, "box_width": 4, "box_height": 2},
                               "Medium": {"size": 18, "mines": 40, "box_width": 2, "box_height": 1},
                               "Hard": {"size": 24, "mines": 99, "box_width": 2, "box_height": 1}}

        settings = difficulty_settings.get(option)

        self.size_matrix = settings.get("size")
        self.mines = settings.get("mines")
        self.box_width = settings.get("box_width")
        self.box_height = settings.get("box_height")

        self.first_move = True

        self.ventana = tk.Tk()
        self.ventana.title("Minesweeper")
        self.ventana.resizable(False, False)

        bg_header = "darkgreen"
        fg_header = "white"
        font_header = "Arial, 10"

        self.header = tk.Frame(self.ventana, bg=bg_header, height=40)
        self.header.grid(row=0, column=0, sticky="ew")

        self.label_difficulty = tk.Label(
            self.header, text=option, fg=fg_header, bg=bg_header, font=font_header)
        self.label_difficulty.pack(side="left", padx=20, pady=10)

        self.time_counter = tk.Label(self.header, text="00:00",
                                     bg=bg_header, fg=fg_header, font=font_header)
        self.time_counter.pack(side="left", expand=True, padx=10, pady=10)

        self.flags_counter = tk.Label(
            self.header, text=self.mines, bg=bg_header, fg=fg_header, font=font_header)
        self.flags_counter.pack(side="right", padx=20, pady=10)

        self.game_frame = tk.Frame(self.ventana, bg="gray")
        self.game_frame.grid(row=1, column=0, sticky="nsew")

        self.box_conteiner = BoxConteiner(self.size_matrix)
        self.create_boxes()

        self.generate_random_mines()

    def start(self):
        """Start the window"""
        self.ventana.mainloop()

    def create_boxes(self):
        "create the box"
        for y in range(self.size_matrix):
            for x in range(self.size_matrix):
                label = tk.Label(self.game_frame,
                                 width=self.box_width, height=self.box_height, borderwidth=2,
                                 relief="ridge", bg="lightgray")
                label.grid(row=y, column=x, padx=1, pady=1)
                label.bind("<Button-1>", self.click_box)
                label.bind("<Button-3>", self.toggle_flag_in_box)
                box = Box(label, x, y)
                self.box_conteiner.add_box(box)
        self.ventana.update()
        self.aling_center_root(self.ventana)

    def generate_random_mines(self):
        """Generate the mines and introduces it to the box"""

    def click_box(self, event):
        """Box clicked"""
        box: Box = self.__get_box_with_event(event)
        box.click()

    def toggle_flag_in_box(self, event):
        """Set flag in the box"""
        box: Box = self.__get_box_with_event(event)
        box.toggle_flag()

    def __get_box_with_event(self, event):
        label: tk.Label = event.widget
        x = label.grid_info()['column']
        y = label.grid_info()['row']
        box = self.box_conteiner.get_box(x, y)
        return box

    @staticmethod
    def aling_center_root(root: tk.Tk):
        """Centar the root"""
        width_root = root.winfo_width()
        height_root = root.winfo_height()

        width_window = root.winfo_screenwidth()
        height_window = root.winfo_screenheight()

        x = (width_window - width_root) // 2
        y = (height_window - height_root) // 2

        root.geometry(f"{width_root}x{height_root}+{x}+{y}")
