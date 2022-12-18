#!/usr/bin/env python3
from __future__ import annotations
from enum import Enum
import fileinput
import math
import re
from typing import Tuple

DIRECTIONS = {
    'U': (0, 1), 
    'R': (1, 0),
    'D': (0, -1),
    'L': (-1, 0),
}

def sign(x: int) -> int:
    return 0 if x == 0 else x // abs(x)

class Point(object):
    def __init__(self, point: Point = None) -> None:
        self.x = point.x if point else 0
        self.y = point.y if point else 0

    def move(self, direction: Tuple[int, int]) -> None:
        self.x += direction[0] 
        self.y += direction[1] 

    def vector(self, other: Point) -> Point:
        return (other.x - self.x, other.y - self.y)


    def follow(self, other: Point) -> None:
        vector = self.vector(other)
        if  vector[0] ** 2 + vector[1] ** 2 >= 4:
            self.move((sign(vector[0]), sign(vector[1])))

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y


class Rope(object):
    __move_regex = re.compile('^(?P<direction>[URDL]) (?P<steps>\d+)')

    def __init__(self, knots: int) -> None:
        self.knots = [Point() for _ in range(knots)]
        self.tail_positions = set()

    def move(self, move: str) -> None:
        group = self.__move_regex.match(move)
        direction = DIRECTIONS[group['direction']]
        for _ in range(int(group['steps'])):
            self.knots[0].move(direction)
            for i in range(1, len(self.knots)):
                self.knots[i].follow(self.knots[i - 1])
            self.tail_positions.add(Point(self.knots[-1]))

if __name__ == '__main__':
    movements = [line.strip() for line in fileinput.input()]

    # part 1
    test_rope = Rope(2)
    test_rope.move('R 4')
    test_rope.move('U 4')
    test_rope.move('L 3')
    test_rope.move('D 1')
    test_rope.move('R 4')
    test_rope.move('D 1')
    test_rope.move('L 5')
    test_rope.move('R 2')
    assert len(test_rope.tail_positions) == 13

    rope = Rope(2)
    for movement in movements:
        rope.move(movement)
    print(f'Tail of rope with 2 knots has been in {len(rope.tail_positions)}')

    # part 2
    test_rope = Rope(10)
    test_rope.move('R 5')
    test_rope.move('U 8')
    test_rope.move('L 8')
    test_rope.move('D 3')
    test_rope.move('R 17')
    test_rope.move('D 10')
    test_rope.move('L 25')
    test_rope.move('U 20')
    assert len(test_rope.tail_positions) == 36

    rope = Rope(10)
    for movement in movements:
        rope.move(movement)
    print(f'Tails of rope with 10 knots has been in {len(rope.tail_positions)}')
