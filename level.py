from constants import *
#from tile import Tile
from bubble import Bubble
class Level:
    def __init__(self):
        self.x = 40
        self.y = 25
        self.columns = COLUMNS
        self.rows = ROWS
        self.bubble_width = BUBBLE_WIDTH
        self.bubble_height = BUBBLE_WIDTH
        self.row_height = 28
        self.row_offset = 0
        self.radius = self.bubble_width / 2
        self.width = self.columns * self.bubble_width + self.bubble_width / 2
        self.grid = []

        for i in range(self.rows):
            new_row = []
            for j in range(self.columns):
                #new_row.append(Tile(i,j,-1))
                new_row.append(Bubble(i,j,0,0,-1,False))
            self.grid.append(new_row)

    def random_level(self):
        for i in range(self.rows):
            random_bubble = random.randint(0,len(COLORS)-1)
            count = 0
            for j in range(self.columns):
                if count >= 2:
                    new_bubble = random.randint(0,len(COLORS)-1)
                    if new_bubble == random_bubble:
                        new_bubble = (new_bubble + 1) % len(COLORS)
                    random_bubble = new_bubble
                    count = 0
                count += 1
                if i < self.rows / 2:
                    self.grid[i][j].bubble_color = random_bubble
                else:
                    self.grid[i][j].bubble_color = -1
        return

