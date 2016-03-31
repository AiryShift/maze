from random import shuffle, randrange
from copy import copy
from Coordinate import Coordinate

POSSIBLE_MOVES = [Coordinate(0, 1),
                  Coordinate(0, -1),
                  Coordinate(1, 0),
                  Coordinate(-1, 0)]


class GenerationError(Exception):
    def __init__(self, msg):
        return super().__init__(msg)


class Cell():
    """
    Describes a cell in the maze

    self.walls[coord] is True if that wall is broken
    """

    def __init__(self, visited=False):
        self._visited = visited
        self.walls = {coord: False for coord in POSSIBLE_MOVES}

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value

    def break_wall(self, coord):
        self.walls[coord] = True

    def broken_walls(self):
        for wall, is_broken in self.walls.items():
            if is_broken:
                yield wall

    def count_broken_walls(self):
        return sum(self.walls.values())


class Maze():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cell_maze = None

    def _can_break_wall(self, at, to):
        # at_cell = self.cell_maze[at.x][at.y]
        to_cell = self.cell_maze[to.x][to.y]
        if to_cell.visited:
            return False
        return True

    def _find_moves(self, coord):
        my_moves = copy(POSSIBLE_MOVES)
        shuffle(my_moves)
        for move in my_moves:
            possibility = coord + move
            if 0 <= possibility.x < self.h and 0 <= possibility.y < self.w:
                yield possibility

    def _make_cell_maze(self):
        self.cell_maze = [[Cell() for _ in range(self.w)]
                          for _ in range(self.h)]
        todo = [Coordinate(randrange(0, self.h), randrange(0, self.w))]

        while len(todo):
            at_coord = todo[-1]
            at_cell = self.cell_maze[at_coord.x][at_coord.y]
            at_cell.visited = True

            for new_coord in self._find_moves(at_coord):
                new_cell = self.cell_maze[new_coord.x][new_coord.y]
                if self._can_break_wall(at_coord, new_coord):
                    new_cell.break_wall(new_coord - at_coord)
                    at_cell.break_wall(at_coord - new_coord)
                    todo.append(new_coord)
                    break
            else:
                todo.pop()

    @classmethod
    def _convert_coord(cls, row, col):
        return Coordinate(*[2 * (i + 1) - 1 for i in (row, col)])

    def make_maze(self, *, remake=False):
        """
        Returns a boolean array representing a maze
        True for path, False for walls
        Each cell is padded with walls in the following configuration
        w w w
        w c w
        w w w
        """
        if not (self.w >= 3 and self.h >= 3):
            raise GenerationError(
                'width: {} and height: {} must be greater than 3'.format(
                    self.w, self.h))

        if remake or self.cell_maze is None:
            self._make_cell_maze()
        bool_maze = [[False for _ in range(2 * self.w + 1)]
                     for _ in range(2 * self.h + 1)]

        for row_num, row in enumerate(self.cell_maze):
            for cell_num, cell in enumerate(row):
                new_coord = Maze._convert_coord(row_num, cell_num)
                bool_maze[new_coord.x][new_coord.y] = True
                for broken_wall in cell.broken_walls():
                    breaking = new_coord + broken_wall
                    bool_maze[breaking.x][breaking.y] = True
        return bool_maze

if __name__ == '__main__':
    import sys
    w, h = 75, 40
    if len(sys.argv) >= 3:
        w, h = map(int, sys.argv[1:])
    out = Maze(w, h)
    for i in out.make_maze():
        for j in i:
            print('#' if not j else '.', end='')
        print()
