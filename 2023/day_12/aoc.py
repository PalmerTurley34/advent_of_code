from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
import json
from functools import cache

@cache
def check_permutation(springs: str, numbers: str) -> int:
    if '?' not in springs:
        return is_valid_permutation(springs, numbers)
    change_i = springs.index('?')
    with_dot = springs[:change_i] + '.' + springs[change_i+1:]
    with_hash = springs[:change_i] + '#' + springs[change_i+1:]
    return check_permutation(with_dot, numbers) + check_permutation(with_hash, numbers)

@cache
def is_valid_permutation(springs: str, numbers: str) -> int:
    '''
    this function assumes that there is no ? characters in springs
    make sure to only call after validating there a no ? characters
    '''
    # print(springs)
    numbers = json.loads(numbers)
    if springs.count('#') != sum(numbers):
        return False
    num_i = 0
    i = 0
    while i < len(springs) and num_i < len(numbers):
        curr_num = numbers[num_i]
        if springs[i] != '#':
            i += 1
            continue
        if springs[i: i+curr_num].count('#') == curr_num:
            if i+curr_num < len(springs) and springs[i+curr_num] != '.':
                return 0 
            num_i += 1
            i += curr_num
        else:
            return 0
    # print(springs)
    return 1

@cache
def count_permutations(springs: str, numbers_str: str) -> int:
    numbers: list[int] = json.loads(numbers_str)
    num = numbers[0]
    counts = 0
    if len(numbers) == 1:
        if springs.count('#') > num or len(springs) < num:
            return counts
        for i in range(num, len(springs)+1):
            spring_slice = springs[i-num: i]
            if '.' in spring_slice:
                continue
            all_count = springs.count('#')
            slice_count = spring_slice.count('#')
            if all_count != slice_count:
                continue
            counts += 1
        # print(springs)
        # print(numbers)
        # print(counts, '\n')
        return counts
    slice_end = (sum(numbers[1:]) + len(numbers[1:]))
    possible_slices = springs[:-slice_end]
    for i in range(num, len(possible_slices)+1):
        if '.' in possible_slices[i-num: i] or '#' in springs[i] or '#' in possible_slices[:i-num]:
            continue
        counts += count_permutations(springs[i+1:], json.dumps(numbers[1:]))
    # print(springs)
    # print(numbers)
    # print(counts, '\n')
    return counts


with open('inputs.txt') as f:
    lines = [line.strip() for line in f]

total_variations = 0
for line_count, line in enumerate(lines):
    springs, numbers = line.split()
    # get rid of dots at beginning and end, they are irrelevant
    # list is easier to mutate
    springs = list(springs)
    numbers = [int(item) for item in numbers.split(',')]
    numbers = numbers * 5
    springs_cp = springs.copy()
    for _ in range(4):
        springs = springs + ['?'] + springs_cp
    # print(f'{"".join(springs)} {",".join([str(num) for num in numbers])}')
    # print('???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3')
    # print(numbers)
    # print(springs)
    changes_made = True
    while changes_made:
        if not springs or not numbers:
            springs = []
            total_variations += 1
            break
        if numbers[0] == len(springs):
            total_variations += 1
            springs = []
            break
        changes_made = False
        # remove areas before/after dots from beginning/end
        if '.' in springs[:numbers[0]]:
            spring_slice = springs[:numbers[0]]
            cut_index = len(spring_slice) - spring_slice[::-1].index('.')
            springs = springs[cut_index:]
            if not springs or not numbers:
                springs = []
                total_variations += 1
                break
            if numbers[0] == len(springs):
                total_variations += 1
                springs = []
                break
            changes_made = True
        if '.' in springs[-numbers[-1]:]:
            cut_index = springs.index('.', -numbers[-1])
            springs = springs[:cut_index]
            if not springs or not numbers:
                springs = []
                total_variations += 1
                break
            if numbers[0] == len(springs):
                total_variations += 1
                springs = []
                break
            changes_made = True
        # ffill/bfill where # has to be placed
        if '#' in springs[:numbers[0]]:
            fill_start = springs.index('#')
            springs[fill_start:numbers[0]] = ['#'] * (numbers[0] - fill_start)
            # changes_made = True
        if '#' in springs[-numbers[-1]:]:
            spring_slice = springs[-numbers[-1]:]
            fill_end = len(springs) - spring_slice[::-1].index('#')
            springs[-numbers[-1]:fill_end] = ['#'] * (fill_end - (len(springs) - numbers[-1]))
            # changes_made = True
        # remove questions marks from beginning/end that can't be possible
        if springs[numbers[0]] == '#':
            i = numbers[0] + 1
            while i < len(springs) and springs[i] == '#':
                i += 1
            springs = springs[i-numbers[0]:]
            if not springs or not numbers:
                springs = []
                total_variations += 1
                break
            if numbers[0] == len(springs):
                total_variations += 1
                springs = []
                break
            changes_made = True
        if springs[-numbers[-1] - 1] == '#':
            i = len(springs) - numbers[-1] - 2
            while i > 0 and springs[i] == '#':
                i -= 1
            springs = springs[:i+numbers[-1]+1]
            if not springs or not numbers:
                springs = []
                total_variations += 1
                break
            if numbers[0] == len(springs):
                total_variations += 1
                springs = []
                break
            changes_made = True
        # remove numbers and springs if first and last start with #
        # +/- 1 to account for the dot
        if springs[0] == '#':
            springs = springs[numbers.pop(0)+1:]
            if not springs or not numbers:
                springs = []
                total_variations += 1
                break
            if numbers[0] == len(springs):
                total_variations += 1
                springs = []
                break
            changes_made = True
        if springs[-1] == '#':
            springs = springs[:(-numbers.pop(-1))-1]
            if not springs or not numbers:
                springs = []
                total_variations += 1
                break
            if numbers[0] == len(springs):
                total_variations += 1
                springs = []
                break
            changes_made = True
        # fill overlaps with #
        overlap_count = len(springs) - (sum(numbers) + len(numbers) - 1)
        overlap_nums = [(i, num) for i, num in enumerate(numbers) if num > overlap_count]
        for i, num in overlap_nums:
            begin_nums = numbers[:i+1]
            end_nums = numbers[i:]
            end_i = sum(begin_nums) + len(begin_nums) - 1
            begin_i = -(sum(end_nums) + len(end_nums) - 1)
            springs[begin_i:end_i] = ['#'] * (end_i - (len(springs) + begin_i))
    # print('checking permutations')
    if springs:
        variations = count_permutations(''.join(springs), json.dumps(numbers)) 
        if variations == 0:
            breakpoint()
        # variations_old = check_permutation(''.join(springs), json.dumps(numbers)) 
        # if variations != variations_old:
        #     breakpoint()
        print(f'{line_count}: {variations}')
        total_variations += variations
    else:
        print(f'{line_count}: 1')
    # if line_count % 25 == 0:
    #     print('done 25')
    # print(line_count)
print(total_variations)
    # print(numbers, '\n')