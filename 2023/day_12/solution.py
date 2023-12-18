import json
from functools import cache

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
        return counts
    slice_end = (sum(numbers[1:]) + len(numbers[1:]))
    possible_slices = springs[:-slice_end]
    for i in range(num, len(possible_slices)+1):
        if '.' in possible_slices[i-num: i] or '#' in springs[i] or '#' in possible_slices[:i-num]:
            continue
        counts += count_permutations(springs[i+1:], json.dumps(numbers[1:]))
    return counts

def main(part=1):
    with open('inputs.txt') as f:
        lines = [line.strip() for line in f]

    total_variations = 0
    for line in lines:
        springs, numbers = line.split()
        numbers = [int(item) for item in numbers.split(',')]
        if part == 2:
            repeat = 5
            numbers = numbers * repeat
            springs_cp = springs
            for _ in range(repeat-1):
                springs = springs + '?' + springs_cp
        variations = count_permutations(springs, json.dumps(numbers)) 
        total_variations += variations
    print(f'Part {part}: {total_variations}')

if __name__ == '__main__':
    main()
    main(2)