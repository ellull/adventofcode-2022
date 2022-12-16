#!/usr/bin/env python3
import fileinput
from typing import Set, Tuple

def parse_assignment(assignment: str) -> Set[int]:
    (start, end) = assignment.split("-", 1)
    return set(range(int(start), int(end) + 1))

def parse_pair(pair: str) -> Tuple[Set[int], Set[int]]:
    (assignment1, assignment2) = pair.split(",", 1)
    return (parse_assignment(assignment1), parse_assignment(assignment2))

def part1(assignment1: Set[int], assignment2: Set[int]) -> bool:
    return assignment1.issuperset(assignment2) or assignment2.issuperset(assignment1)

def part2(assignment1: Set[int], assignment2: Set[int]) -> bool:
    return not assignment1.isdisjoint(assignment2)

if __name__ == '__main__':
    pairs = [parse_pair(line.strip()) for line in fileinput.input()]

    assert part1(*parse_pair('2-4,6-8')) == False
    assert part1(*parse_pair('2-3,4-5')) == False
    assert part1(*parse_pair('5-7,7-9')) == False
    assert part1(*parse_pair('2-8,3-7')) == True
    assert part1(*parse_pair('6-6,4-6')) == True
    assert part1(*parse_pair('2-6,4-8')) == False

    fully_overlapping_pairs = sum(part1(*pair) for pair in pairs)
    print(f"Fully overlapping pairs: {fully_overlapping_pairs}")

    overlapping_pairs = sum(part2(*pair) for pair in pairs)
    print(f"Overlapping pairs: {overlapping_pairs}")
