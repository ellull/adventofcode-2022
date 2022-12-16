#!/usr/bin/env python3
from collections import deque
import fileinput
import re
from typing import List

class Stacks(object):
    __move_regex = re.compile('move (?P<moves>\d+) from (?P<orig>\d+) to (?P<dest>\d+)')

    def __init__(self, input: List[str]) -> None:
        columns = sorted(''.join(column)[::-1] for column in zip(*input))
        self._stacks = [deque(column[1:].strip()) for column in columns if '1' <= column[0] <= '9']

    def move_9000(self, movement: str) -> None:
        groups = self.__move_regex.match(movement)
        moves, orig, dest = int(groups['moves']), int(groups['orig']) - 1, int(groups['dest']) - 1

        orig_stack = self._stacks[orig]
        dest_stack = self._stacks[dest]
        dest_stack.extend(orig_stack.pop() for _ in range(moves))

    def move_9001(self, movement: str) -> None:
        groups = self.__move_regex.match(movement)
        moves, orig, dest = int(groups['moves']), int(groups['orig']) - 1, int(groups['dest']) - 1

        orig_stack = self._stacks[orig]
        dest_stack = self._stacks[dest]
        dest_stack.extend(reversed([orig_stack.pop() for _ in range(moves)]))

    def tops(self) -> str:
        return ''.join(stack[-1] for stack in self._stacks)
        

if __name__ == '__main__':
    lines = fileinput.input()

    # read the file header and movements
    header = []
    for line in lines:
        if len(line.strip()) == 0:
            break
        header.append(line)

    movements = [line for line in lines]

    # part 1
    stacks = Stacks([
        '    [D]    ',
        '[N] [C]    ',
        '[Z] [M] [P]',
        ' 1   2   3 ',
    ])
    stacks.move_9000('move 1 from 2 to 1')
    stacks.move_9000('move 3 from 1 to 3')
    stacks.move_9000('move 2 from 2 to 1')
    stacks.move_9000('move 1 from 1 to 2')
    assert stacks.tops() == 'CMZ'

    stacks = Stacks(header)
    for movement in movements:
        stacks.move_9000(movement)
    crates_at_the_top_9000 = stacks.tops()
    print(f"Crates at the top (CrateMover 9000): {crates_at_the_top_9000}")

    # part 2
    stacks = Stacks([
        '    [D]    ',
        '[N] [C]    ',
        '[Z] [M] [P]',
        ' 1   2   3 ',
    ])
    stacks.move_9001('move 1 from 2 to 1')
    stacks.move_9001('move 3 from 1 to 3')
    stacks.move_9001('move 2 from 2 to 1')
    stacks.move_9001('move 1 from 1 to 2')
    assert stacks.tops() == 'MCD'

    stacks = Stacks(header)
    for movement in movements:
        stacks.move_9001(movement)
    crates_at_the_top_9001 = stacks.tops()
    print(f"Crates at the top (CrateMover 9001): {crates_at_the_top_9001}")
