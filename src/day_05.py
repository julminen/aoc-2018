from typing import List, Set, Tuple
from aoc_utils import read_input_file


def shrink(polymer: str, mask: List[bool]) -> int:
    polymer = list(polymer)
    all_done = False
    while not all_done:
        all_done = True
        a = -1
        b = -1
        i = 0
        while i < len(polymer):
            valid = mask[i]
            if valid:
                if a == -1:
                    a = i
                elif b == -1:
                    b = i
                if a > -1 and b > -1:
                    if polymer[a].swapcase() == polymer[b]:
                        mask[a] = False
                        mask[b] = False
                        all_done = False
                        i = b
                        a = -1
                        b = -1
                if b > -1:
                    a = b
                b = -1
            i += 1
    final = ''.join([c for (i, c) in enumerate(polymer) if mask[i]])
    return len(final)


def phase_1(polymer: str) -> int:
    return shrink(polymer, [True] * len(polymer))


def phase_2(polymer: str) -> int:
    results = dict()
    for element in sorted(list(set(polymer.lower()))):
        length = shrink(polymer, [b.lower() != element for b in polymer])
        results[length] = element
        # print(f'{element}: {length}')
    # print(results)
    return min(results.keys())


if __name__ == "__main__":
    polymer = read_input_file('05')[0]
    print(f'Phase 1: {phase_1(polymer)}')
    # 11540
    print(f'Phase 2: {phase_2(polymer)}')
    # 6918
