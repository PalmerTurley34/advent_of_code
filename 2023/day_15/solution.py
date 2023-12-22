from collections import defaultdict
from dataclasses import dataclass

@dataclass
class Lens:
    label: str
    length: int

def get_hash_value(sequence: str) -> int:
    hash_value = 0
    for char in sequence:
        hash_value += ord(char)
        hash_value *= 17
        hash_value %= 256
    return hash_value

def part_1(sequences: list[str]):
    hash_sum = 0
    for sequence in sequences:
        hash_value = get_hash_value(sequence)
        hash_sum += hash_value
    print(f'Part 1: {hash_sum}')

def part_2(sequences: list[str]):
    boxes = defaultdict(list)
    for sequence in sequences:
        if sequence.endswith('-'):
            label = sequence[:-1]
            box = get_hash_value(label)
            for i, lens in enumerate(boxes[box]):
                if lens.label == label:
                    boxes[box].pop(i)
                    break
        else:
            label, lens = sequence.split('=')
            lens_len = int(lens)
            box = get_hash_value(label)
            for i, lens in enumerate(boxes[box]):
                if lens.label == label:
                    boxes[box][i].length = lens_len
                    break
            else:
                boxes[box].append(Lens(label, lens_len))
    calculation = 0
    for i in range(256):
        for j, lens in enumerate(boxes[i]):
            calculation += (i + 1) * (j + 1) * lens.length
    print(f'Part 2: {calculation}')


def main():
    with open('inputs.txt') as file:
        sequences = file.read().strip().split(',')
    part_1(sequences)
    part_2(sequences)


if __name__ == '__main__':
    main()