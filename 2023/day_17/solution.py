import numpy as np 
from enum import StrEnum, auto
from dataclasses import dataclass
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

class Direction(StrEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

@dataclass(frozen=True)
class QueuedLocation:
    location: np.ndarray
    from_direction: Direction
    steps_in_direction: int

    def __hash__(self) -> int:
        return hash((tuple(self.location), self.from_direction, self.steps_in_direction))
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, QueuedLocation):
            return (
                np.array_equal(self.location, __value.location) and
                self.from_direction == __value.from_direction and
                self.steps_in_direction == __value.steps_in_direction
            )
        return False

index_changes = {
    Direction.UP: np.array([-1, 0]),
    Direction.DOWN: np.array([1, 0]),
    Direction.LEFT: np.array([0, -1]),
    Direction.RIGHT: np.array([0, 1])
}

def is_valid_direction(direction: Direction, position: np.ndarray, grid_shape: np.ndarray) -> bool:
    new_position = position + index_changes[direction]
    return 0 <= new_position[0] < grid_shape[0] and 0 <= new_position[1] < grid_shape[1]

def get_possible_directions(curr_direction: Direction, curr_loc: np.ndarray, same_dir_count: int, grid_shape: np.ndarray) -> list[Direction]:
    possible_directions = []
    if curr_direction is None:
        return [Direction.RIGHT, Direction.DOWN]
    if curr_direction == Direction.UP:
        if is_valid_direction(Direction.LEFT, curr_loc, grid_shape):
            possible_directions.append(Direction.LEFT)
        if is_valid_direction(Direction.RIGHT, curr_loc, grid_shape):
            possible_directions.append(Direction.RIGHT)
        if same_dir_count == 3:
            return possible_directions
        if is_valid_direction(Direction.UP, curr_loc, grid_shape):
            possible_directions.append(Direction.UP)
    if curr_direction == Direction.DOWN:
        if is_valid_direction(Direction.LEFT, curr_loc, grid_shape):
            possible_directions.append(Direction.LEFT)
        if is_valid_direction(Direction.RIGHT, curr_loc, grid_shape):
            possible_directions.append(Direction.RIGHT)
        if same_dir_count == 3:
            return possible_directions
        if is_valid_direction(Direction.DOWN, curr_loc, grid_shape):
            possible_directions.append(Direction.DOWN)
    if curr_direction == Direction.RIGHT:
        if is_valid_direction(Direction.UP, curr_loc, grid_shape):
            possible_directions.append(Direction.UP)
        if is_valid_direction(Direction.DOWN, curr_loc, grid_shape):
            possible_directions.append(Direction.DOWN)
        if same_dir_count == 3:
            return possible_directions
        if is_valid_direction(Direction.RIGHT, curr_loc, grid_shape):
            possible_directions.append(Direction.RIGHT)
    if curr_direction == Direction.LEFT:
        if is_valid_direction(Direction.UP, curr_loc, grid_shape):
            possible_directions.append(Direction.UP)
        if is_valid_direction(Direction.DOWN, curr_loc, grid_shape):
            possible_directions.append(Direction.DOWN)
        if same_dir_count == 3:
            return possible_directions
        if is_valid_direction(Direction.LEFT, curr_loc, grid_shape):
            possible_directions.append(Direction.LEFT)
    return possible_directions

def main():
    with open('inputs.txt') as file:
        grid = np.array([list(line.strip()) for line in file], int)
    visited = set()
    start_node = QueuedLocation(np.array([0, 0]), None, 0)
    all_scores = defaultdict(lambda: sys.maxsize)
    all_scores[start_node] = 0
    frontier = {start_node}
    target_group = []
    while frontier:
        curr_location: QueuedLocation = min(frontier, key=lambda x: all_scores[x])
        frontier.remove(curr_location)
        next_directions = get_possible_directions(curr_location.from_direction, curr_location.location, curr_location.steps_in_direction, grid.shape)
        for direction in next_directions:
            new_loc = curr_location.location + index_changes[direction]
            new_dir = direction
            if curr_location.from_direction == direction:
                new_step_count = curr_location.steps_in_direction + 1
            else:
                new_step_count = 1
            next_node = QueuedLocation(new_loc, new_dir, new_step_count)
            if next_node not in visited:
                curr_score = all_scores[next_node]
                new_score = min(all_scores[curr_location] + grid[*new_loc], curr_score)
                all_scores[next_node] = new_score
                frontier.add(next_node)
        visited.add(curr_location)
        if np.array_equal(curr_location.location, np.array([grid.shape[0]-1, grid.shape[1]-1])):
            target_group.append(curr_location)
    end_values = [all_scores[loc] for loc in target_group]

    print(f'Part 1: {min(end_values)}')
    print(f'Part 2: Not yet solved')

if __name__ == '__main__':
    main()