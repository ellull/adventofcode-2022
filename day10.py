#!/usr/bin/env python3
from __future__ import annotations
from abc import ABC, abstractmethod
import fileinput
from typing import Any, Iterable, List

class Instruction(ABC):
    @abstractmethod
    def execute(self, cpu: CPU) -> None:
        pass


class Noop(Instruction):
    def execute(self, cpu: CPU):
        return True

    def __repr__(self) -> str:
        return 'Noop'


class Addx(Instruction):
    def __init__(self, immediate: int) -> None:
        self._cycle = 0
        self._immediate = immediate

    def execute(self, cpu: CPU):
        self._cycle += 1
        if self._cycle == 2:
            cpu.x += self._immediate
            return True
        return False

    def __repr__(self) -> str:
        return f'Addx({self._immediate})'


class CPU(object):
    def __init__(self, program: Iterable[Instruction]) -> None:
        self.x = 1
        self.cycle = 0
        self.probes = []
        self._instruction = next(program)
        self._program = program

    def tick(self) -> None:
        self.cycle += 1

        for probe in self.probes:
            probe(self)

        finished = self._instruction.execute(self)
        if finished:
            self._instruction = next(self._program, None)

    def run(self) -> None:
        while self._instruction:
            self.tick()


class SignalStrengthProbe(object):
    __cycles_set = {20 + 40 * i for i in range(6)}

    def __init__(self) -> None:
        self.signal_strength = 0

    def __call__(self, cpu: CPU) -> None:
        if cpu.cycle in self.__cycles_set:
            self.signal_strength += cpu.cycle * cpu.x


class DrawProbe(object):
    __height = 6
    __width = 40

    def __init__(self) -> None:
        self._screen = ['.' for _ in range(self.__height * self.__width)]
        self._pixel = 0

    def __call__(self, cpu: CPU) -> None:
        if cpu.x - 1 <= self._pixel % self.__width <= cpu.x + 1:
            self._screen[self._pixel] = '#'
        self._pixel += 1

    def print(self) -> None:
        for y in range(self.__height):
            pos = y * self.__width
            print(''.join(self._screen[pos:pos + 39]))


def compile(asm: List[str]) -> Iterable[Instruction]:
    for line in asm:
        if line == 'noop':
            yield Noop()
        elif line[:4] == 'addx':
            yield Addx(int(line[5:]))


if __name__ == '__main__':
    program = compile(line.strip() for line in fileinput.input())

    signal_strength_probe = SignalStrengthProbe()
    draw_probe = DrawProbe()

    cpu = CPU(program)
    cpu.probes.append(signal_strength_probe)
    cpu.probes.append(draw_probe)
    cpu.run()

    print(f'Signal strength: {signal_strength_probe.signal_strength}')
    draw_probe.print()