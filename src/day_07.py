from typing import List, Set, Tuple, Dict
from aoc_utils import read_input_file
import copy

class Node:
    def __init__(self, name):
        self.name = name
        self.pre = list()
        self.post = list()
        self.task_len = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(name) + 1 + 60
    
    def __eq__(self, other):
        return other is not None and self.name == other.name
    
    def __lt__(self, other):
        return other is not None and self.name < other.name
    
    def __str__(self):
        return f'{self.name}: Pre: {self.pre}, Post: {self.post}, task length: {self.task_len}'
    
    def __repr__(self):
        return str(self)
    
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
    ready_nodes: List[Node] = sorted([n for n in graph.values() if not n.pre])
    done: List[str] = list()

    while ready_nodes:
        n = ready_nodes.pop(0)
        n.run(ready_nodes, graph)
        ready_nodes.sort()
        done.append(n.name)
    
    return ''.join(done)


def phase_2(graph: Dict[str, Node], workers: int) -> int:
    runnable_nodes: List[Node] = list()
    task_schedule: Dict[int, Node] = dict()
    current_tick: int
    idle_workers = workers

    for node in sorted([n for n in graph.values() if not n.pre]):
        if idle_workers > 0:
            task_schedule[node.task_len] = [node]
            idle_workers -= 1
        else:
            runnable_nodes.append(node)

    while task_schedule:
        current_tick = min(task_schedule.keys())
        ready_nodes: List[Node] = task_schedule.pop(current_tick)
        idle_workers += len(ready_nodes)
        for rn in ready_nodes:
            rn.run(runnable_nodes, graph)
        runnable_nodes.sort()
        while idle_workers > 0:
            if not runnable_nodes:
                break
            n = runnable_nodes.pop(0)
            work_list: List[Node] = task_schedule.get(n.task_len, list())
            work_list.append(n)
            task_schedule[current_tick + n.task_len] = work_list
            idle_workers = idle_workers - 1

    return current_tick


if __name__ == "__main__":
    lines = read_input_file('07')
    graph = create_graph(lines)
    print(f'Phase 1: {phase_1(copy.deepcopy(graph))}')
    # JDEKPFABTUHOQSXVYMLZCNIGRW
    print(f'Phase 2: {phase_2(graph, workers=5)}')
    # 1048
