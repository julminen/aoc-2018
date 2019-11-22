from typing import List, Set, Tuple, Dict
from aoc_utils import read_input_file
from dataclasses import dataclass
from collections import namedtuple
from PIL import Image, ImageDraw
import colorsys


Box = namedtuple('Box', ['min_x', 'max_x', 'min_y', 'max_y'])
Coordinate = namedtuple('Coordinate', ['x', 'y'])


@dataclass(init=True, order=True, frozen=True)
class Point:
    coord: Coordinate
    id: int

    @staticmethod
    def new(definition: (int, str)):
        row_number, points_str = definition
        x, y = map(int, points_str.split(','))
        return Point(Coordinate(x, y), row_number)

    def distance(self, other: Coordinate) -> int:
        return abs(self.coord.x - other.x) + abs(self.coord.y - other.y)


def get_map_bounds(points: List[Point]) -> Box:
    min_x: int = min([p.coord.x for p in points])
    max_x: int = max([p.coord.x for p in points])
    min_y: int = min([p.coord.y for p in points])
    max_y: int = max([p.coord.y for p in points])
    return Box(min_x, max_x, min_y, max_y)


def draw_map(points: List[Point], area_map: Dict[Coordinate, int], max_area_id):
    # Generate colors
    N = len(points) + 1
    HSV_tuples = [(x/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))

    origins = [p.coord for p in points]
    bounds = get_map_bounds(points)
    img_size = (bounds.max_x + 1, bounds.max_y + 1)
    im = Image.new('RGB', img_size, (255, 255, 255))
    d = ImageDraw.Draw(im)

    for y in range(0, bounds.max_y+1):
        for x in range(0, bounds.max_x+1):
            c = Coordinate(x, y)
            owner_id = area_map[c]
            if owner_id == -1:
                color = (255, 255, 255)
            elif c in origins:
                if owner_id == max_area_id:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 0)
            else:
                color = tuple(int(255 * x) for x in RGB_tuples[owner_id])
            d.point([c.x, c.y], color)

    im.save('day_06_map.png')


def color_bounding_area(points: List[Point]):
    area_map: Dict[Coordinate, int] = dict()
    
    def get_owner(coordinate: Coordinate) -> int:
        closest_point_id = points[0].id
        shortest_distance = points[0].distance(coordinate)
        for p in points[1:]:
            dist = p.distance(coordinate)
            if dist < shortest_distance:
                closest_point_id = p.id
                shortest_distance = dist
            elif dist == shortest_distance:
                closest_point_id = -1
        return closest_point_id

    bounds = get_map_bounds(points)
    for y in range(0, bounds.max_y+1):
        for x in range(0, bounds.max_x+1):
            c = Coordinate(x, y)
            area_map[c] = get_owner(c)
    infinite_ids: Set[int] = set()
    areas: Dict[int, int] = dict()
    for y in range(bounds.min_y, bounds.max_y+1):
        for x in range(bounds.min_x, bounds.max_x+1):
            c = Coordinate(x, y)
            owner_id = area_map[c]
            if y == bounds.min_y or y == bounds.max_y or x == bounds.min_x or x == bounds.max_x:
                infinite_ids.add(owner_id)
            areas[owner_id] = areas.get(owner_id, 0) + 1
    
    filtered_areas = { key:value for (key, value) in areas.items() if key not in infinite_ids }
    # print(f'Areas: {areas}')
    # print(f'Non infinite areas: {filtered_areas}')

    max_area_id = max(filtered_areas, key=filtered_areas.get)
    max_area = filtered_areas[max_area_id]

    draw_map(points, area_map, max_area_id)

    return max_area_id, max_area



def phase_1(points: List[Point]) -> int:
    _max_area_id, max_area = color_bounding_area(points)
    # print(f'max_area_id = {max_area_id}, max_area = {max_area}')
    return max_area


def phase_2(points: List[Point]) -> int:
    return 0


if __name__ == "__main__":
    # points = list(map(Point.new, enumerate(read_input_file('06_example'))))
    points = list(map(Point.new, enumerate(read_input_file('06'))))

    print(f'Phase 1: {phase_1(points)}')
    # 5975
    #
    #print(f'Phase 2: {phase_2(points)}')
