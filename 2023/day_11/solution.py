import numpy as np
from itertools import combinations

def main():
    with open('inputs.txt') as file:
        space = np.array([list(line.strip()) for line in file])
    numbers_space = np.where(space == '#', 1, 0)
    horizontal_expansions = np.where(numbers_space.sum(1) == 0)[0]
    vertical_expansions = np.where(numbers_space.sum(0) == 0)[0]
    galaxies = np.where(space == '#')
    locations = [(x, y) for x, y in zip(galaxies[0], galaxies[1])]
    cartesian_distances = 0
    expansions_crossed = 0
    expansion_constant = 1
    for i, loc1 in enumerate(locations[:-1]):
        for loc2 in locations[i+1:]:
            distance = abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
            horiz_range = range(*sorted([loc1[0], loc2[0]]))
            vert_range = range(*sorted([loc1[1], loc2[1]]))
            horiz_exp_crossed = sum(expansion in horiz_range for expansion in horizontal_expansions)
            vert_exp_crossed = sum(expansion in vert_range for expansion in vertical_expansions)
            cartesian_distances += distance
            expansions_crossed += horiz_exp_crossed + vert_exp_crossed
    
    part_1_expand_dist = 1
    part_2_expand_dist = 999_999
    part_1_answer = cartesian_distances + part_1_expand_dist * expansions_crossed
    part_2_answer = cartesian_distances + part_2_expand_dist * expansions_crossed
    print(f'Part 1: {part_1_answer}')
    print(f'Part 2: {part_2_answer}')
    


if __name__ == '__main__':
    main()