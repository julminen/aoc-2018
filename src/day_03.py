from typing import List
from aoc_utils import read_input_file
from dataclasses import dataclass
import numpy as np


@dataclass(init=False)
class Box:
    id: int
    x: int
    y: int
    w: int
    h: int

    def __init__(self, spec: str):
        parts = spec.split()
        self.id = int(parts[0][1:])
        self.x, self.y = map(int, parts[2].strip(':').split(','))
        self.w, self.h = map(int, parts[3].split('x'))

    def overlaps(self, other) -> bool:
        def range_overlap(a_min, a_max, b_min, b_max):
            return (a_min <= b_max) and (b_min <= a_max)

        return range_overlap(self.x, self.x + self.w, other.x, other.x + other.w) \
               and range_overlap(self.y, self.y  + self.h, other.y, other.y + other.h)


class Canvas:
    def __init__(self, w: int, h: int):
        self.state: np.ndarray = np.zeros(shape=(h, w), dtype=int)

    def add(self, box: Box):
        for y in range(box.h):
            for x in range(box.w):
                self.state[x+box.x][y+box.y] += 1


def part_1(boxes: List[Box]):
    canvas = Canvas(1000, 1000)
    for box in boxes:
        canvas.add(box)
    return len(canvas.state[canvas.state>1])


def part_2(boxes: List[Box]):
    for box_a in boxes:
        collision = False
        for box_b in boxes:
            if box_a.id != box_b.id and box_a.overlaps(box_b):
                collision = True
                break
        if not collision:
            return box_a.id
    return 0


if __name__ == "__main__":
    boxes = list(map(Box, read_input_file('03')))

    print(f'Part 1: {part_1(boxes)}')
    print(f'Part 2: {part_2(boxes)}')
