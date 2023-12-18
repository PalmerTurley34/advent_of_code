import numpy as np
from collections import defaultdict
import operator
from functools import reduce

def main():
    non_symbol_chars = [str(i) for i in range(10)] + ['.']

    part_number_sum = 0
    star_symbols = defaultdict(list)

    with open('inputs.txt') as file:
        schematic = np.array([list(line.strip()) for line in file])

    for i in range(schematic.shape[0]):
        j = 0
        while j < schematic.shape[1]:
            if schematic[i,j].isnumeric():
                k = j + 1
                while k < schematic.shape[1] and schematic[i, k].isnumeric():
                    k += 1
                number = int(''.join(schematic[i, j:k]))
                symbol_field = schematic[max(0, i-1):i+2, max(0,j-1): k+1]
                has_adjacent_symbol = any([char not in non_symbol_chars for char in symbol_field.flatten()])
                if has_adjacent_symbol:
                    part_number_sum += number
                is_gear_ratio_number = '*' in symbol_field.flatten()
                if is_gear_ratio_number:
                    i_offset, j_offset = np.where(symbol_field == '*')
                    i_value = i_offset[0] + max(0, i-1)
                    j_value = j_offset[0] + max(0, j-1)
                    star_symbols[f'{i_value},{j_value}'].append(number)
                j = k
            else:
                j += 1
    print(f'Part 1: {part_number_sum}')
    gear_ratio_sum = sum(
        reduce(operator.mul, gear_nums) 
        for gear_nums in star_symbols.values() if len(gear_nums) == 2
        )
    print(f'Part 2: {gear_ratio_sum}')

if __name__ == '__main__':
    main()