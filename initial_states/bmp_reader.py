from typing import List

from PIL import Image

def read_initial_state_from_bmp_file(filename: str) -> List[List[bool]]:
    if filename.split('.')[-1] != 'bmp':
        raise ValueError('Filename must end with .bmp')

    initial_state = []
    with Image.open(filename) as bmp:
        width, height = bmp.size
        for y in range(height):
            row = []
            for x in range(width):
                pixel = bmp.getpixel((x, y))
                if pixel == (0, 0, 0):
                    row.append(False)
                else:
                    row.append(True)
            initial_state.append(row)
    return initial_state