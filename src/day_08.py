from typing import List, Set, Tuple, Dict, Iterator
from aoc_utils import read_input_file


class Node:
    def __init__(self, spec: Iterator[int]):
        self.child_count: int = next(spec)
        self.metadata_entries: int = next(spec)
        self.children = list()
        self.metadata: List[int] = list()
        self.value: int = None
        for _ in range(self.child_count):
            self.children.append(Node(spec))
        for _ in range(self.metadata_entries):
            self.metadata.append(next(spec))
    
    def __str__(self):
        return f'cc: {self.child_count}, metadata: {self.metadata}, children: {self.children}'
    
    def __repr__(self):
        return str(self)
    
    def recursive_metadata_sum(self) -> int:
        return sum(self.metadata) + sum([c.recursive_metadata_sum() for c in self.children])
    
    def get_value(self) -> int:
        if not self.value:
            if self.child_count == 0:
                self.value = sum(self.metadata)
            else:
                self.value = 0
                for idx in self.metadata:
                    idx -= 1
                    if idx >= 0 and idx < self.child_count:
                        self.value += self.children[idx].get_value()
        return self.value


def construct_tree(tree_spec: str) -> Node:
    spec: List[int] = list(map(int, tree_spec.split()))
    return Node(iter(spec))


def phase_1(root: Node) -> int:
    return root.recursive_metadata_sum()


def phase_2(root: Node) -> int:
    return root.get_value()

if __name__ == "__main__":
    lines = read_input_file('08')
    tree_root: Node = construct_tree(lines[0])
    print(f'Phase 1: {phase_1(tree_root)}')
    # 45750
    print(f'Phase 2: {phase_2(tree_root)}')
    # 23266
