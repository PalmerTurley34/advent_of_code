import numpy as np
from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

def find_maze(grid: np.ndarray, start_i: int, start_j: int, start_direction: Direction) -> np.ndarray:
    maze = np.zeros(grid.shape)
    i = start_i
    j = start_j
    direction = start_direction
    while maze[i, j] == 0:
        char = grid[i, j]
        maze[i, j] = 1
        if char == 'F' and direction == Direction.UP:
            j += 1
            direction = Direction.RIGHT
        elif char == 'F' and direction == Direction.LEFT:
            i += 1
            direction = Direction.DOWN
        elif char == 'J' and direction == Direction.RIGHT:
            i -= 1
            direction = Direction.UP
        elif char == 'J' and direction == Direction.DOWN:
            j -= 1
            direction = Direction.LEFT
        elif char == 'L' and direction == Direction.DOWN:
            j += 1
            direction = Direction.RIGHT
        elif char == 'L' and direction == Direction.LEFT:
            i -= 1
            direction = Direction.UP
        elif char == '7' and direction == Direction.UP:
            j -= 1
            direction = Direction.LEFT
        elif char == '7' and direction == Direction.RIGHT:
            i += 1
            direction = Direction.DOWN
        elif char == '|' and direction == Direction.UP:
            i -= 1
        elif char == '|' and direction == Direction.DOWN:
            i += 1
        elif char == '-' and direction == Direction.RIGHT:
            j += 1
        elif char == '-' and direction == Direction.LEFT:
            j -= 1
        else:
            print("Something didn't work right!!")
            breakpoint()
    return maze

def main():
    with open('inputs.txt') as file:
        grid = np.array([list(line.strip()) for line in file])
    start_location = np.where(grid == 'S')
    start_i = start_location[0][0]
    start_j = start_location[1][0]
    print(grid[start_i, start_j])
    grid[start_i, start_j] = '|' # this replacement is found manually from the input
    maze = find_maze(grid, start_i, start_j, Direction.UP)

    maze_len = np.sum(maze)
    print(f'Part 1: {maze_len//2}')

    maze_grid = np.where(maze == 1, grid, '.')
    num_enclosed = 0
    for row in maze_grid:
        row = ''.join([char for char in row if char != '-'])
        i = 0
        crossed_line = False
        while i < len(row):
            if row[i] != '.':
                crossed_line = True
            elif crossed_line:
                lines_crossed = row[:i].count('FJ') + row[:i].count('L7') + row[:i].count('|')
                if lines_crossed % 2:
                    num_enclosed += 1
            i += 1
    print(f'Part 2: {num_enclosed}')


if __name__ == '__main__':
    main()