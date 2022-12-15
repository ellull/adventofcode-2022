#!/usr/bin/env python3
import fileinput
from typing import Iterable, Set, Tuple, TypeVar

T = TypeVar("T")

def grouped(iterable: Iterable[T], n=2) -> Iterable[Tuple[T, ...]]:
    """s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), ..."""
    return zip(*[iter(iterable)] * n)

def parse_items(items: str) -> Set[str]:
    return set(items)

def parse_rucksack(items: str) -> Tuple[Set[str], Set[str]]:
    boundary = len(items) // 2
    return (parse_items(items[:boundary]), parse_items(items[boundary:]))

def priority(item: str) -> int:
    if 'a' <= item <= 'z':
        return ord(item) - ord('a') + 1
    return ord(item) - ord('A') + 27

def part1(items: str) -> str:
    (compartment1, compartment2) = parse_rucksack(items)
    return priority((compartment1 & compartment2).pop())

def part2(elf1: str, elf2: str, elf3: str) -> int:
    return priority((parse_items(elf1) & parse_items(elf2) & parse_items(elf3)).pop())

if __name__ == '__main__':
    assert part1('vJrwpWtwJgWrhcsFMMfFFhFp') == 16
    assert part1('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL') == 38
    assert part1('PmmdzqPrVvPwwTWBwg') == 42
    assert part1('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn') == 22
    assert part1('ttgJtRGJQctTZtZT') == 20
    assert part1('CrZsJsPPZsGzwwsLwLmpwMDw') == 19

    lines = [line.strip() for line in fileinput.input()]

    sum_item_priorities = sum(part1(line) for line in lines)
    print(f"Sum of item priorities: {sum_item_priorities}")


    assert part2(
        'vJrwpWtwJgWrhcsFMMfFFhFp',
        'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
        'PmmdzqPrVvPwwTWBwg'
        ) == 18
    assert part2(
        'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
        'ttgJtRGJQctTZtZT',
        'CrZsJsPPZsGzwwsLwLmpwMDw'
        ) == 52
    sum_group_priorities = sum(part2(*group) for group in grouped(lines, 3))
    print(f"Sum of group priorities: {sum_group_priorities}")

