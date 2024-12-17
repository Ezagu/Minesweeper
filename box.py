import tkinter as tk


class Box:

    def __init__(self, label: tk.Label, x: int, y: int):

        self.label = label

        self.x = x
        self.y = y

        self.mine = False
        self.flag = False
        self.pressed = False

        self.list_around_boxes = []
        # self.__get_around_boxes()

        self.mines_around = 0
        self.colors = {1: "blue",
                       2: "green",
                       3: "red",
                       4: "violet",
                       5: "brown",
                       6: "lightblue",
                       7: "dark",
                       8: "lightgray"}

    def set_around_boxes(self, list_boxes):
        """Set the list of the around boxes"""
        self.list_around_boxes = list_boxes

    def get_around_boxes(self):
        """Return a list with the index of the around boxes"""
        return self.list_around_boxes

    def set_mine(self):
        """indicates the box that contains a mine"""
        self.mine = True

    def toggle_flag(self):
        """toggle the flag"""
        if self.is_pressed():
            return
        self.flag = not self.flag
        self.label.config(bg="red" if self.flag else "lightgray")

    def is_flag(self):
        """Return if the box contains the flag"""
        return self.flag

    def contains_mine(self):
        """Indicate if the box contains a mine"""
        return self.mine

    def click(self):
        """Actions when the box is clicked"""
        if self.is_flag() or self.is_pressed():
            return
        self.pressed = True
        self.label.config(relief="flat", bg="white")
        print("coord:", self.x, self.y)
        print(self.get_around_boxes())

    def is_pressed(self):
        """Return if the box was pressed"""
        return self.pressed

    def get_x(self):
        """Return the coord x"""
        return self.x

    def get_y(self):
        """Return the coord y"""
        return self.y
