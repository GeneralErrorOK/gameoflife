import copy
import logging
import random
from typing import List, Tuple

from assets.cell import Cell


class Grid:
    def __init__(self, size: int, random_initial_life_ratio: float = 0.2, initial_state: List[List[bool]] = None):
        self.size = size
        self._step = 0
        if random_initial_life_ratio and (random_initial_life_ratio < 0 or random_initial_life_ratio > 1):
            raise ValueError("Initial life ratio must be between 0 and 1.")

        if initial_state:
            self._grid = [[Cell(False) for _ in range(size)] for _ in range(size)]
            for y, row in enumerate(initial_state):
                for x, alive in enumerate(row):
                    self._grid[y][x].alive = alive
        else:
            self._grid = [[Cell((random.random() <= random_initial_life_ratio)) for _ in range(self.size)] for _ in range(size)]

        self._logger = logging.getLogger()

    def get_cell(self, x: int, y: int) -> Cell:
        return self._grid[y][x]

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        candidates = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]
        self._logger.debug(f"Cell: {x}, {y}")
        neighbors = []
        for x, y in candidates:
            if x < 0 :
                x = self.size - 1
            if y < 0 :
                y = self.size - 1
            if x > self.size - 1:
                x = 0
            if y > self.size - 1:
                y = 0
            neighbors.append((x, y))
        self._logger.debug(f"Neighbors: {neighbors}")
        return neighbors

    def get_active_neighbors_count(self, x: int, y: int) -> int:
        neighbors = [(
            self.get_cell(coordinate[0], coordinate[1]),
            coordinate[0],
            coordinate[1]) for coordinate in self.get_neighbors(x, y)]
        active_count = 0
        for neighbor in neighbors:
            cell, x, y = neighbor
            if cell.alive:
                self._logger.debug(f"Cell on {x}, {y} is alive.")
                active_count += 1
        self._logger.debug(f"Active: {active_count}\n")
        return active_count

    def evolve(self):
        self._logger.debug(f"Step: {self._step}")
        new_grid = copy.deepcopy(self._grid)
        for y, row in enumerate(self._grid):
            for x, cell in enumerate(row):
                active_neighbors = self.get_active_neighbors_count(x, y)
                new_grid[y][x].evolve(active_neighbors)
        self._grid = new_grid
