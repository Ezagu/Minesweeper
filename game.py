"""Instantiate a window with the game"""
import random
import tkinter as tk
from box import Box
from box_conteiner import BoxConteiner


class Game:
    """Game class"""

    def __init__(self, option: str):
        """option -> difficulty"""

        self.difficulty = option

        # CONFIG
        difficulty_settings = {"Easy": {"size": 10, "mines": 10, "box_width": 4, "box_height": 2},
                               "Medium": {"size": 18, "mines": 40, "box_width": 2, "box_height": 1},
                               "Hard": {"size": 24, "mines": 99, "box_width": 2, "box_height": 1}}

        settings = difficulty_settings.get(self.difficulty)

        bg_header = "darkgreen"
        fg_header = "white"
        font_header = "Arial, 10"

        # ATRIBUTES
        self.size_matrix = settings.get("size")
        self.mines = settings.get("mines")
        self.box_width = settings.get("box_width")
        self.box_height = settings.get("box_height")
        self.flags_counter = self.mines
        self.game_lose = False
        self.game_win = False
        self.game_started = False
        self.boxes_without_mines = []
        self.index_mines = []
        self.timer = 0

        # GUI
        self.ventana = tk.Tk()
        self.ventana.title("Minesweeper")
        self.ventana.resizable(False, False)

        self.header = tk.Frame(self.ventana, bg=bg_header, height=40)
        self.header.grid(row=0, column=0, sticky="ew")

        self.label_difficulty = tk.Label(
            self.header, text=option, fg=fg_header, bg=bg_header, font=font_header)
        self.label_difficulty.pack(side="left", padx=20, pady=10)

        self.time_counter_label = tk.Label(self.header, text="00:00",
                                           bg=bg_header, fg=fg_header, font=font_header)
        self.time_counter_label.pack(
            side="left", expand=True, padx=10, pady=10)

        self.flags_counter_label = tk.Label(
            self.header, bg=bg_header, fg=fg_header, font=font_header)
        self.flags_counter_label.pack(side="right", padx=20, pady=10)
        self.__update_flag_counter_label()

        self.game_frame = tk.Frame(self.ventana, bg="gray")
        self.game_frame.grid(row=1, column=0, sticky="nsew")

        self.box_conteiner = BoxConteiner(self.size_matrix)
        self.create_boxes()

    def create_boxes(self):
        "create the box"

        for y in range(self.size_matrix):
            for x in range(self.size_matrix):
                label = tk.Label(self.game_frame,
                                 width=self.box_width, height=self.box_height, borderwidth=2,
                                 relief="ridge", bg="lightgray")
                label.bind("<Button-1>", self.click_box)
                label.bind("<Button-3>", self.toggle_flag_in_box)
                label.grid(row=y, column=x, padx=1, pady=1)
                box = Box(label, x, y)
                self.box_conteiner.add_box(box)
        self.ventana.update()
        self.aling_center_root(self.ventana)

    def click_box(self, event):
        """Box clicked"""
        if self.game_lose:
            return

        box: Box = self.__get_box_with_event(event)

        print("contains mine:", box.contains_mine())
        print("contains flag:", )

        if box.contains_mine() and not box.get_flag():
            # LOSE
            box.label.config(bg="red")
            self.game_over()

        if not self.game_started:
            # First move
            self.first_move(box)
            return

        if box.is_pressed():
            # Box already pressed
            if self.box_conteiner.get_flags_around_box(box) == box.get_mines_around():
                if self.box_conteiner.all_mines_around_with_flag(box):
                    self.box_conteiner.press_all_around(box)
                else:
                    for ind in box.get_around_boxes_list():
                        box_around: Box = self.box_conteiner.get_box(
                            ind[0], ind[1])
                        if box_around.contains_mine() and not box_around.get_flag():
                            box_around.label.config(bg="red")
                    self.game_over()
        else:
            # Press the box
            self.box_conteiner.press_box_and_comprobate_around(box)

        if self.box_conteiner.how_many_unpressed_boxes() == self.mines:
            # WIN
            self.win()

    def first_move(self, box: Box):
        """The first click in a box, start the game"""
        self.boxes_without_mines = box.get_around_boxes_list()
        self.boxes_without_mines.append((box.get_x(), box.get_y()))
        self.generate_random_mines()
        self.box_conteiner.press_box_and_comprobate_around(box)
        self.update_timer()
        self.game_started = True

    def generate_random_mines(self):
        """Generate the mines and introduces it to the box"""
        while len(self.index_mines) < self.mines:
            x = random.randint(0, self.size_matrix - 1)
            y = random.randint(0, self.size_matrix - 1)
            index = (x, y)
            if index not in self.boxes_without_mines and index not in self.index_mines:
                self.index_mines.append(index)
        for ind in self.index_mines:
            box: Box = self.box_conteiner.get_box(ind[0], ind[1])
            box.put_mine()
        self.box_conteiner.update_mines_around_box()

    def toggle_flag_in_box(self, event):
        """Set flag in the box"""
        box: Box = self.__get_box_with_event(event)
        is_flag = box.get_flag()
        if is_flag:
            box.set_flag(False)
            self.flags_counter += 1
        elif self.flags_counter > 0:
            box.set_flag(True)
            self.flags_counter -= 1
        self.__update_flag_counter_label()

    def update_timer(self):
        """Start the time counter"""
        if self.game_lose or self.game_win:
            return
        self.ventana.after(1000, self.update_timer)
        self.timer += 1
        self.time_counter_label.config(text=self.get_time())

    def get_time(self):
        "Return a string of the time in minutes and seconds"
        segundos = self.timer % 60
        minutos = self.timer // 60
        return f"{minutos}:{segundos:02d}"

    def start(self):
        """Start the window"""
        self.ventana.mainloop()

    def toplevel(self):
        """Show top level when the game is over"""

        top_level = tk.Toplevel(self.ventana)
        # top_level.geometry("300x200")
        top_level.resizable(False, False)
        top_level.title("Win")
        top_level.configure(bg="gray22")

        label_congrats = tk.Label(
            top_level, text="Congrats! You win" if self.game_win else "You lose",
            font="Arial 14 bold", fg="white", bg="gray22")
        label_congrats.pack(pady=15)

        if self.game_win:
            label_time = tk.Label(
                top_level, text=self.get_time(), font="12", fg="white", bg="gray22")
            label_time.pack()

        buttons_frame = tk.Frame(top_level, bg="gray22")
        buttons_frame.pack(pady=10, padx=20)

        reset_button = tk.Button(
            buttons_frame, command=self.reset_game, text="Reset")
        reset_button.pack(side="left", padx=5)

        menu_button = tk.Button(
            buttons_frame, command=self.to_menu, text="Menu")
        menu_button.pack(side="left", padx=5)

        quit_button = tk.Button(
            buttons_frame, command=self.quit, text="Quit")
        quit_button.pack(side="left", padx=5)

        top_level.wait_visibility()
        self.aling_center_root(top_level)

    def reset_game(self):
        """Reset the game"""
        self.ventana.destroy()
        new_game = Game(self.difficulty)
        new_game.start()

    def to_menu(self):
        """Go to the menu and close the game"""
        self.ventana.destroy()
        from gui import Gui
        menu = Gui()
        menu.start()

    def quit(self):
        """Quit the game"""
        self.ventana.destroy()

    def game_over(self):
        """Lose the game"""
        self.game_lose = True
        self.box_conteiner.press_all_mines()
        self.toplevel()

    def win(self):
        """Win the game"""
        self.game_win = True
        self.toplevel()

    def __update_flag_counter_label(self):
        """Update the level of the flags counter"""
        self.flags_counter_label.config(text=str(self.flags_counter))

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
