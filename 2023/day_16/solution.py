import numpy as np 
from enum import StrEnum, auto

class Direction(StrEnum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()

index_changes = {
    Direction.UP: np.array([-1, 0]),
    Direction.DOWN: np.array([1, 0]),
    Direction.LEFT: np.array([0, -1]),
    Direction.RIGHT: np.array([0, 1])
}

new_direction_map = {
    ('/', Direction.LEFT): Direction.DOWN,
    ('/', Direction.RIGHT): Direction.UP,
    ('/', Direction.UP): Direction.RIGHT,
    ('/', Direction.DOWN): Direction.LEFT,
    ('\\', Direction.LEFT): Direction.UP,
    ('\\', Direction.RIGHT): Direction.DOWN,
    ('\\', Direction.UP): Direction.LEFT,
    ('\\', Direction.DOWN): Direction.RIGHT,
    ('-', Direction.UP): Direction.RIGHT,
    ('-', Direction.DOWN): Direction.RIGHT,
    ('-', Direction.LEFT): Direction.LEFT,
    ('-', Direction.RIGHT): Direction.RIGHT,
    ('|', Direction.UP): Direction.UP,
    ('|', Direction.DOWN): Direction.DOWN,
    ('|', Direction.RIGHT): Direction.UP,
    ('|', Direction.LEFT): Direction.UP,
}

def count_illuminated(grid: np.ndarray, start: tuple[np.ndarray, Direction]) -> int:
    illuminated = np.zeros(grid.shape, np.int8)
    refractions = [start]
    been_refracted = set()
    while refractions:
        curr_pos, direction = refractions.pop(0)
        visited = set()
        while 0 <= curr_pos[0] < grid.shape[0] and 0 <= curr_pos[1] < grid.shape[1]:
            if (tuple(curr_pos), direction) in visited:
                break
            visited.add((tuple(curr_pos), direction))
            illuminated[*curr_pos] = 1
            char = grid[*curr_pos]
            if char == '|' and (direction == Direction.LEFT or direction == Direction.RIGHT):
                if tuple(curr_pos) not in been_refracted:
                    refractions.append((curr_pos + index_changes[Direction.DOWN], Direction.DOWN))
                    been_refracted.add(tuple(curr_pos))
            if char == '-' and (direction == Direction.UP or direction == Direction.DOWN):
                if tuple(curr_pos) not in been_refracted:    
                    refractions.append((curr_pos + index_changes[Direction.LEFT], Direction.LEFT))
                    been_refracted.add(tuple(curr_pos))
            direction = new_direction_map.get((char, direction), direction)
            curr_pos = curr_pos + index_changes[direction]
    return illuminated.sum()



def main():
    with open('inputs.txt') as file:
        grid = np.array([list(line.strip()) for line in file])
    part_1 = count_illuminated(grid, (np.array([0, 0]), Direction.RIGHT))
    print(f'Part 1: {part_1}')
    
    max_illuminated = 0
    for i in range(grid.shape[0]):
        max_illuminated = max(max_illuminated, count_illuminated(grid, (np.array([i, 0]), Direction.RIGHT)))
        max_illuminated = max(max_illuminated, count_illuminated(grid, (np.array([i, grid.shape[1]-1]), Direction.LEFT)))
    for j in range(grid.shape[1]):
        max_illuminated = max(max_illuminated, count_illuminated(grid, (np.array([0, j]), Direction.DOWN)))
        max_illuminated = max(max_illuminated, count_illuminated(grid, (np.array([grid.shape[0]-1, j]), Direction.UP)))
    print(f'Part 2: {max_illuminated}')

if __name__ == '__main__': 
    main()