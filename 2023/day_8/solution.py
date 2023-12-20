from dataclasses import dataclass
from math import lcm

@dataclass
class Node:
    left: str
    right: str

def part_1(nodes: dict[str, Node], instructions: str):
    curr_node = 'AAA'
    steps = 0
    instructions_mod = len(instructions)
    while curr_node != 'ZZZ':
        step_direction = instructions[steps % instructions_mod]
        if step_direction == 'R':
            curr_node = nodes[curr_node].right
        else:
            curr_node = nodes[curr_node].left
        steps += 1
    print(f'Part 1: {steps}')

def part_2(nodes: dict[str, Node], instructions: str):
    curr_nodes = [node for node in nodes if node.endswith('A')]
    all_steps = []
    instructions_mod = len(instructions)
    for node in curr_nodes:
        curr_node = node
        steps = 0
        while not curr_node.endswith('Z'):
            step_direction = instructions[steps % instructions_mod]
            if step_direction == 'R':
                curr_node = nodes[curr_node].right
            else:
                curr_node = nodes[curr_node].left
            steps += 1
        all_steps.append(steps)
    steps_lcm = lcm(*all_steps)
    print(f'Part 2: {steps_lcm}')
    

def main():
    with open('inputs.txt') as file:
        lines = [line.strip() for line in file]
    instructions = lines[0]
    node_definitions = lines[2:]
    nodes: dict[str, Node] = {}
    for node_def in node_definitions:
        name, connections = node_def.split(' = ')
        left_conn, right_conn = connections.strip('()').split(', ')
        nodes[name] = Node(left_conn, right_conn)
    part_1(nodes, instructions)
    part_2(nodes, instructions)

if __name__ == '__main__':
    main()