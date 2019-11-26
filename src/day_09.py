from typing import List, Set, Tuple, Dict, Iterator
from aoc_utils import read_input_file
from collections import namedtuple
import sys

MarbleGame = namedtuple('MarbleGame', ['players', 'max_marble', 'hiscore'])

# 10 players; last marble is worth 1618 points: high score is 8317
# 13 players; last marble is worth 7999 points: high score is 146373
# 17 players; last marble is worth 1104 points: high score is 2764
# 21 players; last marble is worth 6111 points: high score is 54718
# 30 players; last marble is worth 5807 points: high score is 37305

games = [
    MarbleGame(players=9, max_marble=25, hiscore=32),
    MarbleGame(players=10, max_marble=1618, hiscore=8317),
    MarbleGame(players=13, max_marble=7999, hiscore=146373),
    MarbleGame(players=17, max_marble=1104, hiscore=2764),
    MarbleGame(players=21, max_marble=6111, hiscore=54718),
    MarbleGame(players=30, max_marble=5807, hiscore=37305)
]

class Marble:
    def __init__(self, id: int):
        self.id = id
        self.previous = self
        self.next = self
    
    def __str__(self):
        return f'{self.previous.id} <- {self.id} -> {self.next.id}'

    def insert_after(self, new):
        new.previous = self
        new.next = self.next
        self.next.previous = new
        self.next = new
    
    def detach(self):
        self.next.previous = self.previous
        self.previous.next = self.next
    
    def get_prev(self, steps):
        if steps == 0:
            return self
        return self.previous.get_prev(steps-1)


def print_list(root: Marble):
    start_id = root.id
    n = root
    i = 0
    while n.next.id != start_id:
        print(f'{n.id} ', end='')
        n = n.next
        i += 1
    print(f'{n.id}')


def play(game: MarbleGame) -> int:
    scores: Dict[int, int] = dict({0:0})
    root = Marble(0)
    current = root
    for i in range(1, game.max_marble+1):
        if game.max_marble > 100000 and i % 10000 == 0:
            print(f'{i} marbles: {i/game.max_marble*100:.04}% done...')
        player = (i-1) % game.players + 1
        if i % 23 == 0:
            rmnode = current.get_prev(7)
            current = rmnode.next
            rmnode.detach()
            scores[player] = scores.get(player, 0) + i + rmnode.id
        else:
            new = Marble(i)
            current.next.insert_after(new)
            current = new
    return max(scores.values())


# 411 players; last marble is worth 71058 points
# What would the new winning Elf's score be if the number of the last marble were
# 100 times larger?
if __name__ == "__main__":
    if len(sys.argv) == 2:
        game = games[int(sys.argv[1])]
    elif len(sys.argv) == 3:
        game = MarbleGame(players=int(sys.argv[1]), max_marble=int(sys.argv[2]), hiscore=None)
    else:
        game = MarbleGame(players=411, max_marble=71058, hiscore=None)
    res = play(game)
    print(game)
    if game.hiscore and game.hiscore != res:
        print(f'Expecting result to be {game.hiscore} but it was {res}')
    else:
        print(f'Result: {res}')