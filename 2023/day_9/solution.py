import numpy as np 

def main():
    with open('inputs.txt') as file:
        lines = [line.strip() for line in file]
    next_value_sums = 0
    prev_value_sums = 0
    for line in lines:
        nums = np.array([int(item) for item in line.split()])
        
        curr_row = nums
        next_num = 0
        while np.any(curr_row):
            next_num += curr_row[-1]
            curr_row = np.diff(curr_row)
        next_value_sums += next_num


        curr_row = nums[::-1]
        prev_num = 0
        while np.any(curr_row):
            prev_num += curr_row[-1]
            curr_row = np.diff(curr_row)
        prev_value_sums += prev_num
    print(f'Part 1: {next_value_sums}')
    print(f'Part 2: {prev_value_sums}')

if __name__ == '__main__':
    main()