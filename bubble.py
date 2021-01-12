from constants import *
class Bubble:
    def __init__(self, x, y, speed, angle, color, moving):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.bubble_color = color
        self.moving = moving

    def reinitialize(self):
        self.x = SCREEN_WIDTH / 2 - TILE_WIDTH / 2
        self.y = SCREEN_HEIGHT - TILE_WIDTH
        self.speed = 500
        self.angle = 90
        self.bubble_color = random.randint(0,len(COLORS)-1)
        self.moving = False
