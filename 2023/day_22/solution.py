from dataclasses import dataclass, field

@dataclass(frozen=True)
class Location:
    x: int
    y: int
    z: int

@dataclass
class Block:
    id: int
    locations: list[Location] = field(default_factory=list)
    blocks_beneath: list[int] = field(default_factory=list)
    blocks_above: list[int] = field(default_factory=list)

    @staticmethod
    def from_string(id: int, definition: str) -> 'Block':
        first, last = definition.split('~')
        first_loc = Location(*[int(item) for item in first.split(',')])
        last_loc = Location(*[int(item) for item in last.split(',')])
        locations = [first_loc]
        if first_loc == last_loc:
            locations = []
        if first_loc.x != last_loc.x:
            for i in range(first_loc.x + 1, last_loc.x):
                locations.append(Location(i, first_loc.y, last_loc.z))
        elif first_loc.y != last_loc.y:
            for i in range(first_loc.y + 1, last_loc.y):
                locations.append(Location(first_loc.x, i, last_loc.z))
        elif first_loc.z != last_loc.z:
            for i in range(first_loc.z + 1, last_loc.z):
                locations.append(Location(first_loc.x, first_loc.y, i))
        locations.append(last_loc)
        return Block(id, locations)

def get_all_blocks(block_defs: list[str]) -> list[Block]:
    return [Block.from_string(i, definition) for i, definition in enumerate(block_defs)]

def let_the_blockies_hit_the_floor(blocks: list[Block], locations: dict[Location, int]):
    changes_made = True
    while changes_made:
        changes_made = False
        for block in blocks:
            has_landed = False
            for loc in block.locations:
                loc_below = Location(loc.x, loc.y, loc.z-1)

                if (loc_below in locations and locations[loc_below] != block.id) or loc.z == 1:
                    has_landed = True
            if has_landed:
                continue
            new_locations = []
            for loc in block.locations:
                locations.pop(loc)
                new_loc = Location(loc.x, loc.y, loc.z-1)
                new_locations.append(new_loc)
                locations[new_loc] = block.id
            block.locations = new_locations
            changes_made = True

def populate_above_and_beneath(blocks: list[Block], locations: dict[Location, int]):
    for block in blocks:
        for loc in block.locations:
            loc_above = Location(loc.x, loc.y, loc.z+1)
            loc_below = Location(loc.x, loc.y, loc.z-1)
            if loc_below in locations and locations[loc_below] not in block.blocks_beneath and locations[loc_below] != block.id:
                block.blocks_beneath.append(locations[loc_below])
            if loc_above in locations and locations[loc_above] not in block.blocks_above and locations[loc_above] != block.id:
                block.blocks_above.append(locations[loc_above])

def count_blocks_to_disintigrate(blocks: dict[int, Block]) -> int:
    can_be_disinterated = set()
    for block in blocks.values():
        can_disintegrate = True
        for id in block.blocks_above:
            if len(blocks[id].blocks_beneath) < 2:
                can_disintegrate = False
        if can_disintegrate:
            can_be_disinterated.add(block.id)
    return len(can_be_disinterated)

def count_fallen_blocks_after_disintegration(blocks: dict[int, Block]) -> int:
    total_count = 0
    for block in blocks.values():
        blocks_to_check = [*block.blocks_above]
        fallen = {block.id}
        while blocks_to_check:
            block_id = blocks_to_check.pop(0)
            next_block = blocks[block_id]
            if all(b_id in fallen for b_id in next_block.blocks_beneath):
                # total_count += 1
                fallen.add(block_id)
                blocks_to_check += next_block.blocks_above
        total_count += len(fallen) - 1
    return total_count

def main():
    with open('inputs.txt') as file:
        block_defs = [line.strip() for line in file]
    blocks = get_all_blocks(block_defs)
    blocks_dict = {block.id: block for block in blocks}
    locations_dict = {}
    for block in blocks:
        for loc in block.locations:
            locations_dict[loc] = block.id
    let_the_blockies_hit_the_floor(blocks, locations_dict)
    populate_above_and_beneath(blocks, locations_dict)
    disintigrate_count = count_blocks_to_disintigrate(blocks_dict)
    print(f'Part 1: {disintigrate_count}')
    all_fallen_blocks = count_fallen_blocks_after_disintegration(blocks_dict)
    print(f'Part 2: {all_fallen_blocks}')

if __name__ == '__main__':
    main()