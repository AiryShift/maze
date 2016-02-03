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

POSSIBLE_MOVES = [Coordinate(0, 1), Coordinate(
    0, -1), Coordinate(1, 0), Coordinate(-1, 0)]


def _find_moves(coord):
    random.shuffle(POSSIBLE_MOVES)
    for move in POSSIBLE_MOVES:
        yield coord + move


def _bounds_check(coord, w, h):
    return 0 <= coord.x < h and 0 <= coord.y < w


def _is_valid_position(coord, prev, maze):
    """
    Performs a bounds check
    If the filling in this point forms a cycle then it is also invalid
    """
    w, h = len(maze[0]), len(maze)
    if not _bounds_check(coord, w, h):
        return False
    for new_coord in _find_moves(coord):
        if new_coord != prev and _bounds_check(new_coord, w, h):
            if maze[new_coord.x][new_coord.y]:
                return False
    return True


def make_maze(w, h):
    """
    Returns a boolean array representing a maze
    True for path, False for walls
    """
    if not (w >= 3 and h >= 3):
        raise GenerationError(
            'width: {} and height: {} must be greater than 3'.format(w, h))
    maze = [[False for _ in range(w)] for _ in range(h)]

    todo = [Coordinate(random.randrange(0, h), random.randrange(0, w))]
    while len(todo):
        at = todo[-1]
        maze[at.x][at.y] = True
        for new_position in _find_moves(at):
            if _is_valid_position(new_position, at, maze):
                todo.append(new_position)
                break
        else:
            todo.pop()

    return maze

if __name__ == '__main__':
    for i in make_maze(50, 20):
        for j in i:
            print('#' if not j else '.', end='')
        print()
