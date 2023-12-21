import numpy as np

def find_mirror(grid: np.ndarray) -> int | None:
    '''
    `None` return value means no mirror was found.
    `int` return values is the number of rows/columns before mirror line
    '''
    for i, row in enumerate(grid[:-1]):
        if np.array_equal(row, grid[i+1]):
            perfect_mirror = True
            step = 1
            while i - step >= 0 and i + step + 1 < grid.shape[0]:
                if not np.array_equal(grid[i-step], grid[i+step+1]):
                    perfect_mirror = False
                    break
                step += 1
            if perfect_mirror:
                return i + 1
            
def find_smudge(grid: np.ndarray) -> int | None:
    '''
    `None` return value means no mirror was found.
    `int` return values is the number of rows/columns before mirror line
    '''
    for i, row in enumerate(grid[:-1]):
        if np.sum(np.abs(row - grid[i+1])) > 1:
            continue
        if np.array_equal(row, grid[i+1]):
            num_smudges = 0
        else:
            num_smudges = 1
        step = 1
        while i - step >= 0 and i + step + 1 < grid.shape[0]:
            num_smudges += np.sum(np.abs(grid[i-step] - grid[i+step+1]))
            step += 1
        if num_smudges == 1:
            return i + 1

def main():
    with open('inputs.txt') as file:
        grids = file.read().split('\n\n')
        grids = [np.array([list(line) for line in grid.split('\n')]) for grid in grids]
    summary = 0
    smudge_summary = 0
    for grid in grids:
        grid = np.where(grid == '#', 1, 0)
        row_found = find_mirror(grid)
        smudge_row = find_smudge(grid)
        col_found = find_mirror(grid.T)
        smudge_col = find_smudge(grid.T)
        if row_found is not None:
            summary += 100 * row_found
        elif col_found is not None:
            summary += col_found
        if smudge_row is not None:
            smudge_summary += 100 * smudge_row
        elif smudge_col is not None:
            smudge_summary += smudge_col
    
    print(f'Part 1: {summary}')
    print(f'Part 2: {smudge_summary}')

if __name__ == '__main__':
    main()