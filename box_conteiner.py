"""Conteiner that contains all the boxes of the game in a matrix"""
from box import Box


class BoxConteiner:
    """The box conteiner"""

    def __init__(self, size: int):
        self.size = size
        self.boxes_matrix = [[None for _ in range(self.size)]
                             for _ in range(self.size)]

    def add_box(self, box: Box):
        """Add box to the matrix"""
        x = box.get_x()
        y = box.get_y()
        self.boxes_matrix[x][y] = box
        self.__set_boxes_around_box(box)

    def get_box(self, x: int, y: int):
        """Return box with the coords"""
        return self.boxes_matrix[x][y]

    def update_mines_around_box(self):
        """Comprobate if there are mines around the box and put it in a variable in the box"""
        for j in range(self.size):
            for i in range(self.size):
                box: Box = self.get_box(i, j)
                if box.contains_mine():
                    continue
                boxes_around = box.get_around_boxes_list()
                counter = 0
                for ind in boxes_around:
                    box_around: Box = self.get_box(ind[0], ind[1])
                    if box_around.contains_mine():
                        counter += 1
                box.set_mines_around(counter)

    def get_flags_around_box(self, box: Box):
        """Return how many flags are around the box"""
        counter = 0
        for ind in box.get_around_boxes_list():
            box_around: Box = self.get_box(ind[0], ind[1])
            if box_around.get_flag():
                counter += 1
        return counter

    def all_mines_around_with_flag(self, box: Box):
        """Return True if all the boxes around the box that contains a mine has a flag"""
        for ind in box.get_around_boxes_list():
            box_around: Box = self.get_box(ind[0], ind[1])
            if not box_around.get_flag() and box_around.contains_mine():
                return False
        return True

    def press_all_around(self, box: Box):
        """Press all the boxes around the box"""
        for ind in box.get_around_boxes_list():
            box_around: Box = self.get_box(ind[0], ind[1])
            self.press_box_and_comprobate_around(box_around)

    def press_box_and_comprobate_around(self, box: Box):
        """press the box and press the boxes that has not mines around"""
        if box.click():
            if box.get_mines_around() == 0:
                self.press_all_around(box)

    def how_many_unpressed_boxes(self):
        """Return how many boxes are unpressed"""
        counter = 0

        for j in range(self.size):
            for i in range(self.size):
                box: Box = self.get_box(i, j)
                if not box.is_pressed():
                    counter += 1

        return counter

    def press_all_mines(self):
        """Press all the boxes that contains a mine"""
        for j in range(self.size):
            for i in range(self.size):
                box: Box = self.get_box(i, j)
                if box.contains_mine():
                    box.click()

    def __set_boxes_around_box(self, box: Box):
        """Get the index of the around boxes of the box and set it in the box"""
        list_boxes = []
        for sum_y in range(-1, 2):
            for sum_x in range(-1, 2):
                if sum_y == 0 and sum_x == 0:
                    # Same box
                    continue
                x = box.get_x() + sum_x
                y = box.get_y() + sum_y
                if x < 0 or y < 0 or x > self.size - 1 or y > self.size - 1:
                    continue
                list_boxes.append((x, y))
        box.set_around_boxes_list(list_boxes)
