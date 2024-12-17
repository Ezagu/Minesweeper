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
                list_boxes.append({x: y})
        box.set_around_boxes(list_boxes)
