from PIL import Image
import numpy as np
from maze import Maze

SIZE_OF_SQUARE = 15
BLACK = 0
WHITE = 255


def render(w, h, out='a.png'):
    maze = Maze(w, h)
    w, h = (i * 2 + 1 for i in (w, h))
    bitmap = np.zeros((h * SIZE_OF_SQUARE, w * SIZE_OF_SQUARE), dtype='uint8')
    for x, row in enumerate(maze.make_maze()):
        for y, cell in enumerate(row):
            colour = WHITE if cell else BLACK
            if x == 0 and y == 1 or x == h - 1 and y == w - 2:
                colour = WHITE
            elif x == 0 or y == 0 or x == h - 1 or y == w - 1:
                colour = BLACK
            bX, bY = (i * SIZE_OF_SQUARE for i in (x, y))
            bitmap[bX:bX + SIZE_OF_SQUARE, bY:bY + SIZE_OF_SQUARE] = colour
    rendered_image = Image.fromarray(bitmap)
    rendered_image.save(out, "PNG")

if __name__ == '__main__':
    import time
    start = time.time()
    import sys
    w, h = 50, 20
    if len(sys.argv) >= 3:
        w, h = map(int, sys.argv[1:])
    render(w, h)
    print('Rendered with width {} and height {}'.format(w, h))
    print('Took {:.5} seconds'.format(time.time() - start))
