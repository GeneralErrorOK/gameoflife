import sys
from dataclasses import dataclass
from typing import Tuple
import argparse
import logging
import pygame

from assets.grid import Grid
from initial_states.bmp_reader import read_initial_state_from_bmp_file


def get_square_size(screen_size: Tuple[int, int], grid_size: int) -> int:
    smallest_dim = min(screen_size)
    square_size = smallest_dim // grid_size
    return square_size


def create_background(bg_size: Tuple[int, int]):
    background = pygame.Surface(bg_size)
    background = background.convert()
    background.fill((10, 10, 10))
    return background


def render_grid(grid: Grid, square_size: int, surface: pygame.Surface) -> pygame.Surface:
    start_x, start_y = 0, 0
    for x in range(0, grid.size):
        for y in range(0, grid.size):
            rect = pygame.Rect(start_x + (x * square_size), start_y + (y * square_size), square_size, square_size)
            if grid.get_cell(x, y).alive:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)
            pygame.draw.rect(surface, color, rect)
    return surface


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grid-size", type=int, help="Set grid size. Grid is square. (Default = 100x100)")
    parser.add_argument("-w", "--window-size", type=int, help="Set window size. Window is square. (Default = 800x800)")
    parser.add_argument("-f", "--file", type=str, help="Read initial state from BMP file. Reads grid size from file as well.")
    parser.add_argument("-r", "--ratio", type=float, help="Set live:dead ratio when using random initial state. (Example: \"0.2\")")
    parser.add_argument("-s", "--speed", type=int, help="Speed of animation in frames per second. (Default: 10fps)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.grid_size:
        grid_size = args.grid_size
    else:
        grid_size = 100

    if args.window_size:
        screen_size = args.window_size, args.window_size
    else:
        screen_size = 800, 800

    if args.speed:
        speed = args.speed
    else:
        speed = 10

    if args.ratio:
        seed_ratio = args.ratio
    else:
        seed_ratio = 0.2

    if args.file:
        initial_state = read_initial_state_from_bmp_file(args.file)
        grid_size = len(initial_state)
        grid = Grid(grid_size, initial_state=initial_state)
    else:
        grid = Grid(grid_size, random_initial_life_ratio=seed_ratio)

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Willem's Game of Life")
    clock = pygame.time.Clock()

    background = create_background(screen.get_size())
    square_size = get_square_size(screen.get_size(), grid_size)

    background = render_grid(grid, square_size, background)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # Do logical updates here.
        grid.evolve()

        # Render frame here
        render_grid(grid, square_size, background)
        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()
