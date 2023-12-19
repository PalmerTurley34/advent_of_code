from dataclasses import dataclass, field
from collections import defaultdict
import operator
from functools import reduce

@dataclass
class RangeMap:
    dest_start: int
    src_start: int
    range_len: int
    dest_end: int = field(init=False)
    src_end: int = field(init=False)
    offset: int = field(init=False)

    def __post_init__(self):
        self.dest_end = self.dest_start + self.range_len
        self.src_end = self.src_start + self.range_len
        self.offset = self.dest_start - self.src_start

def get_next_layer_ranges(seed_range: range, range_maps: list[RangeMap]) -> list[range]:
    next_layer_ranges = []
    for range_map in range_maps:
        if seed_range.start >= range_map.src_end:
            continue
        if seed_range.stop < range_map.src_end:
            next_layer_ranges.append(range(seed_range.start + range_map.offset, seed_range.stop + range_map.offset))
            seed_range = None
            break
        else:
            next_layer_ranges.append(range(seed_range.start + range_map.offset, range_map.dest_end))
            seed_range = range(range_map.src_end, seed_range.stop)
    if seed_range:
        next_layer_ranges.append(seed_range)
    return next_layer_ranges

def parse_layer_range_maps(mapping: str) -> list[RangeMap]:
    ranges = mapping.split('\n')[1:]
    range_maps = [RangeMap(*[int(item) for item in line.split()]) for line in ranges]
    return range_maps

def create_complete_layer(range_maps: list[RangeMap]) -> list[RangeMap]:
    '''
    fill in the gaps where there is no offset and sort all the maps
    creating a complete layer of range maps
    '''
    range_maps = sorted(range_maps, key=lambda r: r.src_start)
    to_append = []
    if range_maps[0].src_start != 0:
        to_append.append(RangeMap(0, 0, range_maps[0].src_start))
    for i in range(1, len(range_maps)):
        curr_range = range_maps[i]
        prev_range = range_maps[i-1]
        if curr_range.src_start != prev_range.src_end:
            to_append.append(RangeMap(prev_range.src_end, prev_range.src_end, curr_range.src_start - prev_range.src_end))
    range_maps = sorted(range_maps + to_append, key=lambda r: r.src_start)
    return range_maps

def main(part=1):
    with open('inputs.txt') as file:
        inputs = file.read().split('\n\n')
    seeds = [int(num) for num in inputs[0].strip('seeds: \n').split()]
    if part == 1:
        seed_ranges = [range(seed, seed+1) for seed in seeds]
    else:
        seed_ranges = [range(seed_start, seed_start+seed_end) for seed_start, seed_end in zip(seeds[::2], seeds[1::2])]
    all_range_maps = []
    mappings = inputs[1:]
    for mapping in mappings:
        range_maps = parse_layer_range_maps(mapping)
        range_maps = create_complete_layer(range_maps)
        all_range_maps.append(range_maps)

    curr_layer_ranges = seed_ranges
    for range_mappings in all_range_maps:
        curr_layer_ranges = reduce(operator.add, [get_next_layer_ranges(seed_range, range_mappings) for seed_range in curr_layer_ranges])

    min_range = min(curr_layer_ranges, key=lambda r: r.start)
    print(f'Part {part}: {min_range.start}')


if __name__ == '__main__':
    main()
    main(2)