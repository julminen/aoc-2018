from typing import List, Set, Tuple, Dict
from aoc_utils import read_input_file


class Node:
    def __init__(self, name):
        self.name = name
        self.pre = list()
        self.post = list()
    
    def __eq__(self, other):
        return other is not None and self.name == other.name
    
    def __lt__(self, other):
        return other is not None and self.name < other.name
    
    def __str__(self):
        return f'{self.name}: Pre: {self.pre}, Post: {self.post}'
    
    def __repr__(self):
        return f'{self.name}: pre {self.pre}, post: {self.post}'
    
    def run(self, ready_nodes, graph):
        if self.pre:
            raise ValueError(f'Nonfinished predecessors for node {self.name}: {self.pre}')
        for p in self.post:
            pn = graph[p]
            pn.pre.remove(self.name)
            if not pn.pre:
                ready_nodes.append(pn)


def create_graph(lines: List[str]) -> Dict[str, Node]:
    nodes: Dict[str, Node] = dict()
    for l in lines:
        tokens = l.split()
        pre_name = tokens[1]
        post_name = tokens[7]

        pre_node: Node = nodes.get(pre_name)
        if pre_node == None:
            pre_node = Node(pre_name)
            nodes[pre_name] = pre_node
        pre_node.post.append(post_name)
        
        post_node: Node = nodes.get(post_name)
        if post_node == None:
            post_node = Node(post_name)
            nodes[post_name] = post_node
        post_node.pre.append(pre_name)
    return nodes


def phase_1(graph: Dict[str, Node]) -> str:
    ready_nodes: List[Node] = sorted([n for n in graph.values() if len(n.pre) == 0])
    done: List[str] = list()

    while ready_nodes:
        n = ready_nodes.pop(0)
        n.run(ready_nodes, graph)
        ready_nodes.sort()
        done.append(n.name)
    
    return ''.join(done)


if __name__ == "__main__":
    lines = read_input_file('07')
    graph = create_graph(lines)
    print(f'Phase 1: {phase_1(graph)}')
