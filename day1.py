#!/usr/bin/env python3
import fileinput

def read(iterable):
    elves_calories = []
    elf_calories = 0
    for line in iterable:
        line = line.strip()
        if not line:
            elves_calories.append(elf_calories)
            elf_calories = 0
            continue
        elf_calories += int(line)
    return elves_calories


if __name__ == '__main__':
    top_three = sorted((elf_calories for elf_calories in read(fileinput.input())), reverse=True)[:3]
    
    max_calories = top_three[0]
    print(f"Max calories: {max_calories}")

    top_three_calories = sum(top_three)
    print(f"Top 3 calories: {top_three_calories}")
