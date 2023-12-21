import numpy as np 

def roll_rocks(grid: np.ndarray) -> np.ndarray:
    round_rocks = np.where(grid == 'O')
    for i, j in zip(*round_rocks):
        while i > 0 and grid[i-1, j] == '.':
            grid[i,j] = '.'
            i -= 1
            grid[i,j] = 'O'
    return grid

def main():
    with open('inputs.txt') as file:
        grid = [line.strip() for line in file]
    grid = np.array([list(line) for line in grid])
    for i in range(1_000):
        grid = roll_rocks(grid)
        if i == 0:
            total_load = (grid.shape[0] - np.where(grid == 'O')[0]).sum()
            print(f'Part 1: {total_load}')
        grid = roll_rocks(grid.T).T
        grid = roll_rocks(grid[::-1])[::-1]
        grid = roll_rocks(grid.T[::-1])[::-1].T
        # print(grid)
    total_load = (grid.shape[0] - np.where(grid == 'O')[0]).sum()
    print(f'Part 2: {total_load}')
    #found cycle by manually inspecting input. load after 1000 iterations is same as the correct iteration

if __name__ == '__main__':
    main()