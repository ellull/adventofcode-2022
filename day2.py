#!/usr/bin/env python3
from enum import IntEnum
import fileinput

class Shape(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Result(IntEnum):
    LOOSE = 0
    DRAW = 3
    WIN = 6

oponent_codes = {
    'A': Shape.ROCK,
    'B': Shape.PAPER,
    'C': Shape.SCISSORS,
}

my_codes = {
    'X': Shape.ROCK,
    'Y': Shape.PAPER,
    'Z': Shape.SCISSORS,
}

result_codes = {
    'X': Result.LOOSE,
    'Y': Result.DRAW,
    'Z': Result.WIN,
}

def play(oponent: Shape, me: Shape) -> Result:
    if oponent == me:
        return Result.DRAW
    if (oponent == Shape.ROCK and me == Shape.PAPER) or \
       (oponent == Shape.PAPER and me == Shape.SCISSORS) or \
       (oponent == Shape.SCISSORS and me == Shape.ROCK):
       return Result.WIN
    return Result.LOOSE

def my_shape(oponent: Shape, result: Result) -> Shape:
    if result == Result.DRAW:
        return oponent
    match oponent:
        case Shape.ROCK:
            return Shape.PAPER if result == Result.WIN else Shape.SCISSORS
        case Shape.PAPER:
            return Shape.SCISSORS if result == Result.WIN else Shape.ROCK
        case Shape.SCISSORS:
            return Shape.ROCK if result == Result.WIN else Shape.PAPER

def part1(line: str) -> int:
    oponent = oponent_codes[line[0]]
    me = my_codes[line[2]]
    return me + play(oponent, me)

def part2(line: str) -> int:
    oponent = oponent_codes[line[0]]
    result = result_codes[line[2]]
    return my_shape(oponent, result) + result

if __name__ == '__main__':
    assert part1('A Y') == 8
    assert part1('B X') == 1
    assert part1('C Z') == 6

    lines = list(fileinput.input())

    part1_total_score =sum(part1(line) for line in lines)
    print(f"Part1 total score: {part1_total_score}")

    assert part2('A Y') == 4
    assert part2('B X') == 1
    assert part2('C Z') == 7

    part2_total_score =sum(part2(line) for line in lines)
    print(f"Part1 total score: {part2_total_score}")
