from constants import *


class Bubble:
    even_row_neighbours = [[-1, -1], [-1, 0], [0, 1], [1, 0], [1, -1], [0, -1]]
    odd_row_neighbours = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [0, -1]]

    def __init__(self, x, y, speed, angle, color, moving):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.bubble_color = color
        self.moving = moving
        self.to_remove = False

    def reinitialize(self, x, y, speed, angle, color, moving):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.bubble_color = color
        self.moving = moving
        self.to_remove = False
