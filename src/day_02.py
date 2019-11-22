from typing import List, Dict
from aoc_utils import read_input_file


def count_letters(word: str) -> Dict[str, int]:
    return {k: word.count(k) for k in [c for c in word]}


def common_characters(a: str, b: str) -> List[str]:
    c = list()
    for ch in enumerate(a):
        if b[ch[0]] == ch[1]:
            c.append(ch[1])
    return c


def part_1(boxes: List[str]) -> int:
    twos: int = 0
    threes: int = 0
    for box in boxes:
        counts = count_letters(box)
        twos += 1 if 2 in counts.values() else 0
        threes += 1 if 3 in counts.values() else 0
    return twos * threes


def part_2(boxes: List[str]) -> str:
    for index, a_box in enumerate(boxes):
        for b_box in boxes[index + 1:]:
            commons = common_characters(a_box, b_box)
            if len(commons) + 1 == len(a_box):
                # print(f'Found at {index} for {a_box} and {b_box}')
                return ''.join(commons)


if __name__ == "__main__":
    boxes = read_input_file('02')
    print(f'Part 1: {part_1(boxes)}')
    # 7470
    print(f'Part 2: {part_2(boxes)}')
    # kqzxdenujwcstybmgvyiofrrd
