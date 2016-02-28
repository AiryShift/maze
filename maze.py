import random


class GenerationError(Exception):
    def __init__(self, msg):
        return super().__init__(msg)


class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __str__(self):
        return 'x: {} y: {}'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(repr(self))


POSSIBLE_MOVES = [Coordinate(0, 1), Coordinate(
    0, -1), Coordinate(1, 0), Coordinate(-1, 0)]
w = h = 0


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


def bounds_check(coord):
    return 0 <= coord.x < h and 0 <= coord.y < w


def find_moves(coord):
    random.shuffle(POSSIBLE_MOVES)
    for move in POSSIBLE_MOVES:
        potential_move = coord + move
        if bounds_check(potential_move):
            yield potential_move


def make_cell_maze():
    maze = [[Cell() for _ in range(w)] for _ in range(h)]
    todo = [Coordinate(random.randrange(0, h), random.randrange(0, w))]

    while len(todo):
        at_coord = todo[-1]
        at_cell = maze[at_coord.x][at_coord.y]
        at_cell.visited = True

        for new_coord in find_moves(at_coord):
            new_cell = maze[new_coord.x][new_coord.y]
            if not new_cell.visited:
                # Break the wall relative to the cell
                new_cell.break_wall(new_coord - at_coord)
                at_cell.break_wall(at_coord - new_coord)
                todo.append(new_coord)
                break
        else:
            todo.pop()

    return maze


def convert_coord(row, col):
    return Coordinate(*[2 * (i + 1) - 1 for i in (row, col)])


def make_maze(w_in, h_in):
    """
    Returns a boolean array representing a maze
    True for path, False for walls
    Each cell is padded with walls in the following configuration
    w w w
    w c w
    w w w
    """
    global w, h
    w, h = w_in, h_in
    if not (w >= 3 and h >= 3):
        raise GenerationError(
            'width: {} and height: {} must be greater than 3'.format(w, h))

    cell_maze = make_cell_maze()
    bool_maze = [[False for _ in range(2 * w + 1)] for _ in range(2 * h + 1)]
    for row_num, row in enumerate(cell_maze):
        for cell_num, cell in enumerate(row):
            new_coord = convert_coord(row_num, cell_num)
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
    for i in make_maze(w, h):
        for j in i:
            print('#' if not j else '.', end='')
        print()
