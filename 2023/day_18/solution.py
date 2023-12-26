from collections import defaultdict
import numpy as np

def get_coordinates(directions: list[str], distances: list[int]) -> np.ndarray:
    coordinates = [(0,0)]
    for direction, dist in zip(directions, distances):
        if direction == 'U':
            curr_coord = coordinates[-1]
            new_coord = (curr_coord[0], curr_coord[1] + dist)
            coordinates.append(new_coord)
        if direction == 'D':
            curr_coord = coordinates[-1]
            new_coord = (curr_coord[0], curr_coord[1] - dist)
            coordinates.append(new_coord)
        if direction == 'L':
            curr_coord = coordinates[-1]
            new_coord = (curr_coord[0] - dist, curr_coord[1])
            coordinates.append(new_coord)
        if direction == 'R':
            curr_coord = coordinates[-1]
            new_coord = (curr_coord[0] + dist, curr_coord[1])
            coordinates.append(new_coord)
    vertexes = np.array(coordinates[:-1])
    return vertexes

def get_shoelace_area(vertexes: np.ndarray) -> int:
    x = vertexes[:, 0]
    y = vertexes[:, 1]
    shoelace1 = np.sum(x*np.roll(y,-1))
    shoelace2 = np.sum(y*np.roll(x,-1))
    area = 0.5 * np.abs(shoelace1 - shoelace2)
    return area

directional_map = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}

def main(part=1):
    with open('inputs.txt') as file:
        lines = [line.strip().split() for line in file]
    if part == 1:
        directions = [line[0] for line in lines]
        distances = [int(line[1]) for line in lines]
    else:
        hexes = [line[2].strip('()#') for line in lines]
        directions = [directional_map[hexits[-1]] for hexits in hexes]
        distances = [eval('0x'+ hexits[:5]) for hexits in hexes]
    vertexes = get_coordinates(directions, distances)
    shoelace_area = get_shoelace_area(vertexes)
    # picks theorem: A = i + b/2 - 1
    # solve for (b + i), A = shoelace_area
    latice_points = shoelace_area + (sum(distances) / 2) + 1 
    print(f'Part {part}: {int(latice_points)}')

if __name__ == '__main__':
    main()
    main(2)