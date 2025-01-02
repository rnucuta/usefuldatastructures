import math
import random
from collections import defaultdict

def d(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# special has functions to map
# key to point and reverse, 
# point to key
class specialdict:
    def __init__(self, delta, p1, p2):
        self.map = defaultdict(list)
        self.delta = delta
        self.delta_half = delta/2
        self.closest_pair = [p1, p2]

    def get_key(self, point):
        return (int(point[0] // self.delta_half), int(point[1] // self.delta_half))
                
    def insert(self, point):
        self.map[self.get_key(point)].append(point)

# Section 13.7 of Kleinberg and Tardos: randomized approach
# O(n)
def closest_pair(points):
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