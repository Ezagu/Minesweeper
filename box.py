"""This module contains the class Box, which is the class that represents the boxes of the game."""
import tkinter as tk


class Box:
    """Class that represents the boxes of the game"""

    def __init__(self, label: tk.Label, x: int, y: int):

        self.label: tk.Label = label

        self.x = x
        self.y = y

        self.mine = False
        self.flag = False
        self.pressed = False

        self.list_around_boxes = []

        self.mines_around = 0
        self.colors = {1: "blue",
                       2: "green",
                       3: "red",
                       4: "violet",
                       5: "brown",
                       6: "lightblue",
                       7: "dark",
                       8: "lightgray"}

    def set_around_boxes_list(self, list_boxes):
        """Set the list of the around boxes"""
        self.list_around_boxes = list_boxes

    def get_around_boxes_list(self):
        """Return a list with the index of the around boxes"""
        return self.list_around_boxes

    def put_mine(self):
        """indicates the box that contains a mine"""
        self.mine = True

    def set_flag(self, b: bool):
        """Set the flag"""
        if self.is_pressed():
            return False
        self.flag = b

        self.label.config(bg="indianred" if b else "lightgray")

    def get_flag(self):
        """Return if the box contains the flag"""
        return self.flag

    def contains_mine(self):
        """Indicate if the box contains a mine"""
        return self.mine

    def click(self):
        """Press the box"""
        if self.get_flag() or self.is_pressed():
            return False
        self.pressed = True
        self.label.config(relief="flat")
        if self.contains_mine():
            self.label.config(text="*")
        else:
            self.label.config(bg="white")
        if self.get_mines_around() != 0:
            self.label.config(text=str(self.get_mines_around()),
                              fg=self.colors[self.get_mines_around()])

        return True

    def is_pressed(self):
        """Return if the box was pressed"""
        return self.pressed

    def get_x(self):
        """Return the coord x"""
        return self.x

    def get_y(self):
        """Return the coord y"""
        return self.y

    def set_mines_around(self, mines):
        """Set how many mines has around"""
        self.mines_around = mines

    def get_mines_around(self):
        """Return how many mine there are around the box"""
        return self.mines_around
