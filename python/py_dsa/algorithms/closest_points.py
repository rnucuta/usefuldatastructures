import math
import random
from collections import defaultdict
from typing import Tuple, List, Union


def d(
    point1: Union[List[float], Tuple[float, float]],
    point2: Union[List[float], Tuple[float, float]],
) -> float:
    """Calculates Euclidean distance between two points"""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


class specialdict:
    """Maps a point to a bucket of points within a delta by delta square"""

    def __init__(self, delta: float, p1: Tuple[float, float], p2: Tuple[float, float]):
        self.map = defaultdict(list)
        self.delta = delta
        self.delta_half = delta / 2
        self.closest_pair = [p1, p2]

    def get_key(self, point: Tuple[float, float]) -> Tuple[float, float]:
        """Maps point to a key, which represents a cell in the grid of points"""
        return (int(point[0] // self.delta_half), int(point[1] // self.delta_half))

    def insert(self, point: Tuple[float, float]) -> None:
        """Helper function, adds point to its respective bucket"""
        self.map[self.get_key(point)].append(point)


# Section 13.7 of Kleinberg and Tardos: randomized approach
# O(n)
# TODO: add further explanation
def closest_pair(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Finds the closest pair of points in a list of points using a randomized approach.

    The algorithm first shuffles the list of points to ensure randomness. It then iterates
    through the shuffled list, starting from the second point (index 1). For each point, it
    checks the 25 squares surrounding it (5x5 grid centered at the point) to find the closest
    point that is less than the current minimum distance (delta). If a closer point is found,
    it updates the minimum distance and the pair of points.

    The key insight here is that the closest pair of points must be within a distance of delta
    from each other. This allows us to limit our search to the 25 squares surrounding each point,
    significantly reducing the number of comparisons needed, which leads to an amortized O(n)
    solution (with a large constant).

    Args:
        points: list of all 2D points represented as tuples

    Returns:
        List of pair of points representing the closest two points

    """
    # shuffle points, make copy to not edit the original lists
    shuffled_points = points[:]
    random.shuffle(shuffled_points)

    # calculate initial delta and initialize the first dict
    delta = d(shuffled_points[0], shuffled_points[1])
    map = specialdict(delta, shuffled_points[0], shuffled_points[1])
    map.insert(shuffled_points[0])
    map.insert(shuffled_points[1])

    # for the next 2...n points, check the 25 closest
    # squares. Find the closest element in these
    # 25 squares that is less than delta, and initialize
    # new dict
    for i in range(2, len(shuffled_points)):
        pi = shuffled_points[i]
        S_st_x, S_st_y = map.get_key(pi)
        closest_distance = None
        closest_point = None

        # check 25 squares
        for dx in range(-2, 3):
            surrounding_x = S_st_x + dx
            for dy in range(-2, 3):
                surrounding_y = S_st_y + dy
                if (surrounding_x, surrounding_y) in map.map:
                    for pj in map.map[(surrounding_x, surrounding_y)]:
                        d_t = d(pj, pi)
                        if d_t < map.delta:
                            if closest_distance is None or d_t < closest_distance:
                                closest_distance = d_t
                                closest_point = pj

        if closest_distance is not None:
            map = specialdict(closest_distance, pi, closest_point)
            # reinitialize dict with all points up to current pi
            for pk in range(i + 1):
                map.insert(shuffled_points[pk])
        else:
            map.insert(pi)

    return map.closest_pair
