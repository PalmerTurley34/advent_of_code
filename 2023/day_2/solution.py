from collections import defaultdict
import operator
from functools import reduce

def main():
    max_values = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    valid_game_sum = 0
    power_sums = 0
    for line in open('inputs.txt'):
        game, all_cubes = line.strip().split(': ')
        game_id = int(game.strip('Game '))
        rounds = all_cubes.split('; ')
        cube_counts = reduce(operator.add, [round.split(', ') for round in rounds])
        valid_game = True
        cube_minimums = defaultdict(int)
        for cube in cube_counts:
            count, color = cube.split()
            cube_minimums[color] = max(cube_minimums[color], int(count))
            if int(count) > max_values[color]:
                valid_game = False
        game_power = reduce(operator.mul, cube_minimums.values())
        power_sums += game_power
        if valid_game:
            valid_game_sum += game_id
    print(f'Part 1: {valid_game_sum}')
    print(f'Part 2: {power_sums}')

if __name__ == '__main__': 
    main()