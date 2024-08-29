class Cell:
    def __init__(self, alive: bool):
        self.alive = alive

    def evolve(self, alive_neighbours: int):
        """
        At each step in time, the following transitions occur:

        Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        Any live cell with two or three live neighbours lives on to the next generation.
        Any live cell with more than three live neighbours dies, as if by overpopulation.
        Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        :param alive_neighbours: amount of neighbours alive
        :return:
        """
        if self.alive:
            if alive_neighbours < 2 or alive_neighbours > 3:
                self.alive = False
        else:
            if alive_neighbours == 3:
                self.alive = True

