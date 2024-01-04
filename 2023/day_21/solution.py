import numpy as np
from functools import cache
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +")

movements = {
    'N': Coordinate(-1, 0),
    'S': Coordinate(1, 0),
    'E': Coordinate(0, 1),
    'W': Coordinate(0, -1)
}

def get_counter(grid: np.ndarray):

    @cache
    def count_possibilities(pos: Coordinate, steps: int):
        nonlocal grid
        if not 0 <= pos.x < grid.shape[0] or not 0 <= pos.y < grid.shape[1]:
            return set()
        if grid[pos.x, pos.y] == '#':
            return set()
        if steps == 0:
            return {pos}
        return set.union(*[count_possibilities(pos+movement, steps-1) for movement in movements.values()])

    return count_possibilities
    

def main():
    with open('inputs.txt') as file:
        grid = np.array([list(line.strip()) for line in file])
    start_pos = np.where(grid == 'S')
    start_pos = np.array([*start_pos]).flatten()
    start_pos = Coordinate(*start_pos)
    counter = get_counter(grid)
    num_steps = 64
    possibilities = counter(start_pos, num_steps)
    print(f'Part 1: {len(possibilities)}')
    print(f'Part 2: Not yet implemented')

if __name__ == '__main__':
    main()