import unittest
import json
import sys
sys.path.append("..")

from CMS import CountMinSketch


def process_stream(a, b, p, w, stream):
    """
    Uses the count-min sketch data structure to 
    approximate the count of items in a stream. 
    This is a useful data structure for streaming problems
    where the number of distinct items is large.

    Inputs:
    - a, b: vectors with positive entries with length d
    - p, w: scalar (p), width (w) of the sketch matrix
    - stream: an iterator of items in the stream
    Outputs:
    - a sketch matrix, of size d x w
    """
    cms = CountMinSketch(a, b, p, w)
    for item in stream:
        cms.update(item)
    return cms

class TestCMS(unittest.TestCase):
    def test_simple(self):
        test_problems = [
            ([1,2], [3,5], 100, 3, [10,11,10], [[0, 2, 1], [1, 2, 0]]),
            ([2,3,2,5], [1,10,200,4], 9, 4, [129,  56, 117, 142,  82, 161, 114,  68, 161, 149], [[3, 2, 3, 2], [2, 3, 0, 5], [4, 1, 2, 3], [4, 2, 2, 2]]),
        ]
        for test in test_problems:
            ans = test[-1]
            self.assertListEqual(
                process_stream(a=test[0], b=test[1], p=test[2], w=test[3], stream=iter(test[4])), ans)

    def test_complex(self):
        with open("./inputs/CMS_inputs.json", "rt") as f:
            test_problems = json.load(f)

        for test in test_problems:
            ans = test['ans']
            print(process_stream(a=test['a'], b=test['b'], p=test['p'], w=test['w'], stream=iter(test['stream'])))
            self.assertListEqual(
                process_stream(a=test['a'], b=test['b'], p=test['p'], w=test['w'], stream=iter(test['stream'])), 
                ans)

if __name__ == '__main__':
    unittest.main()
