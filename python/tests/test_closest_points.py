import unittest
from py_dsa.algorithms import closest_pair
from typing import List

input_1 = [(0,0), (1,1), (5,5)]

input_2 = [
    [0.47, 0.53],
    [0.99, 0.54],
    [0.4,  0.57],
    [0.83, 0.19],
    [0.73, 0.1 ],
]

input_3 = [
    [0.8 , 0.62],
    [0.48, 0.56],
    [0.62, 0.77],
    [0.39, 0.22],
    [0.97, 0.46],
    [0.34, 0.56],
    [0.92, 0.45],
    [0.7 , 0.37],
    [0.13, 0.54],
    [0.27, 0.68],
    [0.31, 0.37],
    [0.56, 0.06],
    [0.58, 0.07],
    [0.54, 0.59],
    [0.29, 0.84],
    [0.01, 0.28],
    [0.01, 0.04],
    [0.55, 0.47],
    [0.66, 0.62],
    [0.24, 0.66],
    [0.4 , 0.61],
    [0.55, 0.63],
    [0.7 , 0.05],
    [0.45, 0.16],
    [0.03, 0.07],
    [0.38, 0.03],
    [0.45, 0.15],
    [0.35, 0.53],
    [0.72, 0.47],
    [0.72, 0.33],
    [0.67, 0.12],
    [0.12, 0.33],
    [0.12, 0.7 ],
    [0.46, 0.23],
    [0.17, 0.67],
    [0.49, 0.77],
    [0.65, 0.13],
    [0.17, 0.36],
    [0.69, 0.45],
    [0.06, 0.99],
    [0.95, 0.13],
    [0.52, 0.29],
    [0.06, 0.89],
    [0.39, 0.64],
    [0.54, 0.05],
    [0.6 , 0.19],
    [0.43, 0.76],
    [0.12, 0.03],
    [0.05, 0.6 ],
    [0.44, 0.52],
]

def convert_to_set(points : List[List[int]]):
    return set(tuple(x) for x in points)

class TestClosestPoints(unittest.TestCase):
    def test_closest1(self):
        self.assertEqual(convert_to_set(closest_pair(input_1)), convert_to_set([(0,0), (1,1)]))

    def test_closest2(self):
        self.assertEqual(convert_to_set(closest_pair(input_2)), convert_to_set([[0.47, 0.53], [0.4, 0.57]]))

    def test_closest3(self):
        self.assertEqual(convert_to_set(closest_pair(input_3)), convert_to_set([[0.45, 0.16], [0.45, 0.15]]))

if __name__ == '__main__':
    unittest.main()
