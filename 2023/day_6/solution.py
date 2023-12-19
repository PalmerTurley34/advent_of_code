import numpy as np
import operator
from functools import reduce

def main(part=1):
    with open('inputs.txt') as file:
        lines  = [line.strip() for line in file]
    if part == 1:
        times = [int(item) for item in lines[0].split()[1:]]
        distances = [int(item) for item in lines[1].split()[1:]]
    else:
        times = [int(lines[0].strip('Time: ').replace(' ', ''))]
        distances = [int(lines[1].strip('Distance: ').replace(' ', ''))]
    winning_counts = []
    for time, distance in zip(times, distances):
        # dist = (time - hold_time) * hold_time
        x = np.arange(time)
        dist_traveled = x * (time - x)
        total_win_counts = np.sum(np.where(dist_traveled > distance, 1, 0))
        winning_counts.append(total_win_counts)
    total_product = reduce(operator.mul, winning_counts)
    print(total_product)

if __name__ == '__main__':
    main()
    main(2)