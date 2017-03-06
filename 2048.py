"""
2048 Game Clone
"""
import math
from random import randrange
from random import random

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
UNDO = 5
EXIT = 6
OFFSETS = {UP: (1, 0), DOWN: (-1, 0), LEFT: (0, 1), RIGHT: (0, -1), UNDO: (0, 0), EXIT: (0, 0)}


def merge(line):
    """
    Function that merges a single row or column in 2048
    """
    length = len(line)
    result = [0] * length
    last_index = 0

    for current_index in range(length):
        if line[current_index] != 0:
            result[last_index] = line[current_index]
            last_index += 1

    for key in range(length - 1):
        if z == 3:
            if (result[key] != 0) and (result[key] is result[key + 1]):
                x = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
                y = result[key]
                f = x.index(y)
                result[key] = x[f+1]
                result.pop(key + 1)
                result.append(0)
        else:
            if result[key] is result[key + 1]:
                result[key] *= 2
                result.pop(key + 1)
                result.append(0)

    return result


class TwentyFortyEight:
    """
    Class to run the game
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._is_occupied = False
        self._is_changed = False
        self._grid = None
        self.undo_grid = None
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty
        """
        self._grid = [[0 for this_col in range(self._grid_width)] for this_row in range(self._grid_height)]
        self.undo_grid = [[0 for this_col in range(self._grid_width)] for this_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
        self.get_draw()

    def get_draw(self):
        if z == 2:
            for s in range(self._grid_height):
                a = self._grid[s]
                a = map(int, a)
                for l in range(0, len(a)):
                    if a[l] != 0:
                        a[l] = math.log(a[l], 2)
                    else:
                        a[l] = -48
                    a = map(int, a)
                for j in range(0, len(a)):
                    a[j] += 96
                a = map(chr, a)

                print '||'.join(a)
                print '-----------'
        else:
            for s in range(self._grid_height):
                print '||'.join(map(str, self._grid[s]))
                print '-----------'

    def __str__(self):
        """
        Return a string representation of the grid
        """
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add a new tile if any tiles moved
        """
        offset = OFFSETS[direction]
        temp_grid = []
        # up
        if direction == 1:
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self.undo_grid[row][col] = self._grid[row][col]

            for row in range(self._grid_width):
                start = 0
                temp_list = []
                for this_col in range(self._grid_height):
                    temp_list.append(self._grid[start][row])
                    start += offset[0]
                temp_list = merge(temp_list)
                temp_grid.append(temp_list)

            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = temp_grid[col][row]

        # Down
        elif direction == 2:
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self.undo_grid[row][col] = self._grid[row][col]

            for row in range(self._grid_width):
                start = self._grid_height - 1
                temp_list = []
                for this_col in range(self._grid_height):
                    temp_list.append(self._grid[start][row])
                    start += offset[0]
                temp_list = merge(temp_list)
                temp_grid.append(temp_list)
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = temp_grid[col][self._grid_height - 1 - row]

        # Left
        elif direction == 3:
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self.undo_grid[row][col] = self._grid[row][col]

            for col in range(self._grid_height):
                start = 0
                temp_list = []
                for this_row in range(self._grid_width):
                    temp_list.append(self._grid[col][start])
                    start += offset[1]
                temp_list = merge(temp_list)
                temp_grid.append(temp_list)
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = temp_grid[row][col]

        # Right
        elif direction == 4:
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self.undo_grid[row][col] = self._grid[row][col]

            for col in range(self._grid_height):
                start = self._grid_width - 1
                temp_list = []
                for this_row in range(self._grid_width):
                    temp_list.append(self._grid[col][start])
                    start += offset[1]
                temp_list = merge(temp_list)
                temp_grid.append(temp_list)
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = temp_grid[row][self._grid_width - 1 - col]

        elif direction == 6:
            print "ThankYou for Playing"
            exit(1)

        elif direction == 5:
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = self.undo_grid[row][col]

        if direction != 5:
            total_num = 1
            for value in self._grid:
                for val_el in value:
                    total_num *= val_el
                    if total_num == 0:
                        self._is_occupied = False
                        break
                    else:
                        self._is_occupied = True

            if self._is_changed or not self._is_occupied:
                self.new_tile()
                self._is_changed = False

        self.get_draw()

    def new_tile(self):
        """
        Create a new tile
        """

        while True:
            random_row = randrange(0, self._grid_height)
            random_col = randrange(0, self._grid_width)
            if self._grid[random_row][random_col] is 0:
                print 'New row:', random_row + 1, 'column:', random_col + 1
                if z == 1 or z == 2:
                    self.set_tile(random_row, random_col, 2 if random() < 0.9 else 4)
                elif z == 3:
                    self.set_tile(random_row, random_col, 1 if random() < 0.9 else 2)
                break

    def set_tile(self, row, col, value):
        """
        Set the tile at position [row][col] to the given value
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position [row][col]
        """
        return self._grid[row][col]


if __name__ == '__main__':
    print "1: 2048(2,4,8) 2: Alphabet(a,b,c) 3: Fibonacci(1,2,3,5)"
    print ""
    z=input()
    t = TwentyFortyEight(4, 4)
    while True:
        print '1:Up 2:Down 3:Left 4:Right 5:Undo 6:Exit'
        i = input()
        t.move(i)
