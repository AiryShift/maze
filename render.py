from PIL import Image
import numpy as np
from maze import make_maze

SIZE_OF_SQUARE = 25

def render(w, h, out='a.png'):
    maze = make_maze(w, h)
    bitmap = np.zeros((h * SIZE_OF_SQUARE, w * SIZE_OF_SQUARE))
    for x, row in enumerate(maze):
        for y, cell in enumerate(row):
            colour = 255 if cell else 0
            bX = x * SIZE_OF_SQUARE
            bY = y * SIZE_OF_SQUARE
            for i in range(bX, bX + SIZE_OF_SQUARE):
                for j in range(bY, bY + SIZE_OF_SQUARE):
                    bitmap[i][j] = colour
    bitmap = np.array(bitmap, dtype='uint8')
    rendered_image = Image.fromarray(bitmap)
    rendered_image.save(out, "PNG")

if __name__ == '__main__':
    import sys
    w, h = 50, 20
    if len(sys.argv) >= 3:
        w, h = map(int, sys.argv[1:])
    render(w, h)
