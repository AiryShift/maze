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

    def __init__(self):
        self.visited = False
        self.walls = {coord: False for coord in POSSIBLE_MOVES}

    def visit(self):
        self.visited = True

    def been_visited(self):
        return visited

    def break_wall(self, coord):
        self.walls[coord] = True

    def broken_walls(self):
        for wall, is_broken in walls.items():
            if is_broken:
                yield wall


def _bounds_check(coord):
    return 0 <= coord.x < h and 0 <= coord.y < w


def _find_moves(coord):
    random.shuffle(POSSIBLE_MOVES)
    for move in POSSIBLE_MOVES:
        potential_move = coord + move
        if _bounds_check(potential_move):
            yield potential_move


def _is_valid_position(coord, prev, maze):
    """
    Performs a bounds check
    If filling this point forms a cycle then it is invalid
    If filling this point means a wall has no neighbouring walls it is invalid
    """
    if maze[coord.x][coord.y]:
        return False
    for new_coord in _find_moves(coord):
        if new_coord != prev:
            if maze[new_coord.x][new_coord.y]:  # forms cycle
                return False
            else:  # check for wall neighbours
                neighbours = sum(
                    0 if maze[i.x][i.y] else 1 for i in _find_moves(new_coord))
                if neighbours <= 1:
                    return False
    return True


def make_maze(w_in, h_in):
    """
    Returns a boolean array representing a maze
    True for path, False for walls
    """
    global w
    global h
    w, h = w_in, h_in
    if not (w >= 3 and h >= 3):
        raise GenerationError(
            'width: {} and height: {} must be greater than 3'.format(w, h))
    maze = [[False for _ in range(w)] for _ in range(h)]

    todo = [Coordinate(random.randrange(0, h), random.randrange(0, w))]
    while len(todo):
        at = todo[-1]
        maze[at.x][at.y] = True
        for new_coord in _find_moves(at):
            if _is_valid_position(new_coord, at, maze):
                todo.append(new_coord)
                break
        else:
            todo.pop()

    return maze

if __name__ == '__main__':
    import sys
    w, h = 75, 40
    if len(sys.argv) >= 3:
        w, h = map(int, sys.argv[1:])
    for i in make_maze(w, h):
        for j in i:
            print('#' if not j else '.', end='')
        print()
