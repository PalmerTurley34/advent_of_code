from dataclasses import dataclass
from typing import Literal
from copy import deepcopy

@dataclass
class XmasPart:
    x: str
    m: str
    a: str
    s: str

    @property
    def total_value(self):
        return int(self.x) + int(self.m) + int(self.a) + int(self.s)

    @staticmethod
    def from_string(part_str: str) -> 'XmasPart':
        part_ratings = part_str.strip('{}').split(',')
        ratings = {name: value for name, value in (part.split('=') for part in part_ratings)}
        return XmasPart(**ratings)

@dataclass
class PartRange:
    x: range
    m: range
    a: range
    s: range

    @property
    def total_combinations(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)
    
    def split_range(self, category: Literal['x', 'm', 'a', 's'], operand: Literal['<', '>'], split_value: int) -> 'PartRange':
        curr_range: range = getattr(self, category)
        new_part_range = deepcopy(self)
        if operand == '<':
            range_for_self = range(split_value, curr_range.stop)
            range_for_new = range(curr_range.start, split_value)
        else:
            split_value += 1
            range_for_new = range(split_value, curr_range.stop)
            range_for_self = range(curr_range.start, split_value)
        setattr(self, category, range_for_self)
        setattr(new_part_range, category, range_for_new)
        return new_part_range

@dataclass
class Condition:
    input: str
    output: str

    def eval_condition(self, part: XmasPart) -> bool:
        if self.input is None:
            return True
        category = self.input[0]
        category_rating = getattr(part, category)
        check = self.input.replace(category, category_rating, 1)
        return eval(check)
    
@dataclass
class WorkFlow:
    name: str
    conditions: list[Condition]

    def get_output(self, part: XmasPart) -> str:
        for cond in self.conditions:
            if cond.eval_condition(part):
                return cond.output
            
    @staticmethod
    def from_string(workflow: str) -> 'WorkFlow':
        name, conditions = workflow.strip('}').split('{')
        conditions = conditions.split(',')
        new_conditions = [Condition(*cond.split(':')) for cond in conditions[:-1]] + [Condition(None, conditions[-1])]
        return WorkFlow(name, new_conditions)

def part1(parts: list[XmasPart], workflows: dict[str, WorkFlow]) -> None:
    part_rating_sum = 0
    for part in parts:
        curr = 'in'
        while curr not in ('A', 'R'):
            curr = workflows[curr].get_output(part)
        if curr == 'A':
            part_rating_sum += part.total_value
    print(f'Part 1: {part_rating_sum}')

def part2(workflows: dict[str, WorkFlow]) -> None:
    start_range = PartRange(*([range(1, 4001)]*4))
    total_combs = 0
    part_ranges = [('in', start_range)]
    correct_ranges = []
    while part_ranges:
        workflow_name, part_range = part_ranges.pop(0)
        if workflow_name == 'A':
            total_combs += part_range.total_combinations
            correct_ranges.append(part_range)
            continue
        if workflow_name == 'R':
            continue
        workflow = workflows[workflow_name]
        for cond in workflow.conditions:
            if cond.input is None:
                part_ranges.append((cond.output, part_range))
                continue
            category, operand, value = cond.input[0], cond.input[1], cond.input[2:]
            part_ranges.append((cond.output, part_range.split_range(category, operand, int(value))))
    print(f'Part 2: {total_combs}')


def main():
    with open('inputs.txt') as file:
        rules, parts = file.read().split('\n\n')
    rules = rules.split('\n')
    parts = parts.split('\n')
    workflows = {wf.name: wf for wf in (WorkFlow.from_string(wf_str) for wf_str in rules)}
    parts = [XmasPart.from_string(part) for part in parts]
    part1(parts, workflows)
    part2(workflows)

if __name__ == '__main__':
    main()