import unittest
import sys
sys.path.append("..")

from seq_alignment import sequence_align_fast, sequence_align_slow

class TestSeqAlign(unittest.TestCase):
    def test_align_1(self):
        x = "stop"
        y = "tops"
        def c(x,y):
            return 1 if x != y else 0
        delta = 1.
        alignment = sequence_align_slow(x, y, c, delta)
        self.assertEqual(alignment, ([(2,1), (3,2), (4,3)], 2.0))

    def test_align_2(self):
        x = "stop"
        y = "tops"
        def c(x,y):
            return 1 if x != y else 0
        delta = 1.5
        alignment = sequence_align_slow(x, y, c, delta)
        self.assertEqual(alignment, ([(2,1), (3,2), (4,3)], 3.0))

    def test_align2_1(self):
        x = "stop"
        y = "tops"
        def c(x,y):
            return 1 if x != y else 0
        delta = 1.
        alignment = sequence_align_fast(x, y, c, delta)
        self.assertEqual(alignment, ([(2,1), (3,2), (4,3)], 2.0))

    def test_align2_2(self):
        x = "stop"
        y = "tops"
        def c(x,y):
            return 1 if x != y else 0
        delta = 1.5
        alignment = sequence_align_fast(x, y, c, delta)
        self.assertEqual(alignment, ([(2,1), (3,2), (4,3)], 3.0))

if __name__ == '__main__':
    unittest.main()
