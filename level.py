from constants import *
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
        self.matched_bubbles = []
        self.colors_in_level = set()

        for i in range(self.rows):
            new_row = []
            for j in range(self.columns):
                new_row.append(Bubble(i, j, 0, 0, -1, False))
            self.grid.append(new_row)

    def load_level(self, level_number):
        self.x = 40
        self.y = 25
        self.columns = COLUMNS
        self.rows = ROWS
        fullname = os.path.join("levels", "level" + str(level_number) + ".lvl")
        file = open(fullname, "r")
        line = file.readline().split()
        rows = int(line[0])
        columns = int(line[1])
        for i in range(rows):
            line = file.readline().split()
            for j in range(columns):
                self.grid[i][j].bubble_color = int(line[j])
        self.check_colors_left()

    def match_3(self, x, y):

        self.matched_bubbles.append(self.grid[y][x])
        self.grid[y][x].to_remove = True
        if y % 2:
            # odd row
            neighbours = Bubble.odd_row_neighbours
        else:
            # even row
            neighbours = Bubble.even_row_neighbours
        for neighbour in neighbours:
            if (
                not (
                    x + neighbour[1] < 0
                    or x + neighbour[1] >= self.columns
                    or y + neighbour[0] < 0
                    or y + neighbour[0] >= self.rows
                )
                and not self.grid[y + neighbour[0]][x + neighbour[1]].to_remove
                and self.grid[y + neighbour[0]][x + neighbour[1]].bubble_color
                == self.grid[y][x].bubble_color
            ):
                self.match_3(x + neighbour[1], y + neighbour[0])

    def connected_bubbles(self, x, y):
        self.grid[y][x].to_remove = False
        if y % 2:
            neighbours = Bubble.odd_row_neighbours
        else:
            neighbours = Bubble.even_row_neighbours
        for neighbour in neighbours:
            if (
                not (
                    x + neighbour[1] < 0
                    or x + neighbour[1] >= self.columns
                    or y + neighbour[0] < 0
                    or y + neighbour[0] >= self.rows
                )
                and self.grid[y + neighbour[0]][x + neighbour[1]].to_remove
                and self.grid[y + neighbour[0]][x + neighbour[1]].bubble_color >= 0
            ):
                self.connected_bubbles(x + neighbour[1], y + neighbour[0])

    def remove_floating_bubbles(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j].to_remove = True
        for i in range(self.columns):
            if self.grid[0][i].bubble_color >= 0:
                self.connected_bubbles(i, 0)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].to_remove == True:
                    self.grid[i][j].bubble_color = -1
                    self.grid[i][j].to_remove = False

    def check_colors_left(self):
        self.colors_in_level.clear()
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].bubble_color >= 0:
                    self.colors_in_level.add(self.grid[i][j].bubble_color)

    def check_lose(self):
        for i in range(self.columns):
            if self.grid[self.rows - 1][i].bubble_color >= 0:
                return True
        return False

    def check_win(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j].bubble_color >= 0:
                    return False
        return True