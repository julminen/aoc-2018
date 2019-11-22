from typing import List


def read_input_file(day: str) -> List[str]:
    with open(f'input/{day}_input.txt', 'r') as input_file:
        contents: List[str] = input_file.read().splitlines()
    return contents
