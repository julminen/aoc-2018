from typing import List
from aoc_utils import read_input_file


def part_1(changes: List[int]):
    return sum(changes)


def part_2(changes: List[int]):
    seen_frequencies = set()
    acc: int = 0
    while True:
        for x in changes:
            if acc in seen_frequencies:
                return acc
            seen_frequencies.add(acc)
            acc += x


if __name__ == "__main__":
    changes = list(map(int, read_input_file('01')))
    print(f'Part 1: {part_1(changes)}')
    # 587
    print(f'Part 2: {part_2(changes)}')
    # 83130

