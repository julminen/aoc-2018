from typing import List, Set, Tuple, Dict, Iterator
from aoc_utils import read_input_file
from collections import namedtuple
from PIL import Image, ImageDraw


Box = namedtuple('Box', ['min_x', 'max_x', 'min_y', 'max_y'])


class Point:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    @staticmethod
    def new_from_spec(spec: str):
        x, y = list(map(int, spec[spec.index('<')+1: spec.index('>')].split(',')))
        dx, dy = list(map(int, spec[spec.index('<', spec.index('<')+1)+1: spec.index('>', spec.index('>')+1)].split(',')))
        return Point(x, y, dx, dy)
    
    def __str__(self):
        return f'Point at ({self.x}, {self.y}), going to ({self.dx}, {self.dy})'
    
    def move(self, ticks):
        self.x = self.x + self.dx * ticks
        self.y = self.y + self.dy * ticks 


def get_bounds(points: List[Point]) -> Box:
    min_x = min([p.x for p in points])
    max_x = max([p.x for p in points])
    min_y = min([p.y for p in points])
    max_y = max([p.y for p in points])
    return Box(min_x, max_x, min_y, max_y)


def count_area(points: List[Point]) -> int:
    b = get_bounds(points)
    return (b.max_x - b.min_x) * (b.max_y - b.min_y)


def draw_points(points: List[Point]):
    bounds = get_bounds(points)
    margin = 5
    size = bounds.max_x - bounds.min_x + 2 * margin, bounds.max_y - bounds.min_y + 2 * margin
    img_size = (size[0], size[1])

    im = Image.new('RGB', img_size, (0, 0, 0))
    d = ImageDraw.Draw(im)
    point_color = (0, 255, 100)

    for p in points:
        d.point([p.x - bounds.min_x + margin, p.y - bounds.min_y + margin], point_color)
    im.save('day_10.png')


if __name__ == "__main__":
    lines = read_input_file('10')
    points = list(map(Point.new_from_spec, lines))

    area = count_area(points)
    step = 0
    while True:
        [p.move(1) for p in points]
        new_area = count_area(points)
        if new_area >= area:
            [p.move(-1) for p in points]
            break
        step += 1
        area = new_area
    draw_points(points)
    print(f'1st answer lies in png, {step} seconds were saved')
    # LRCXFXRP
