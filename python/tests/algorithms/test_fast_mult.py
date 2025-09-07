import unittest
from py_dsa.algorithms import reference_multiply, karatsuba, fft
import random

class TestFastMult(unittest.TestCase):
    def test_small(self):
        num = [random.randrange(0, 2, 1) for k in range(20)]
        correct_ans = reference_multiply(num, num)
        self.assertEqual(correct_ans, karatsuba(num, num))
        self.assertEqual(correct_ans, fft(num, num))

    def test_med(self):
        num1 = [random.randrange(0, 2, 1) for k in range(200)]
        num2 = [random.randrange(0, 2, 1) for k in range(200)]
        correct_ans = reference_multiply(num1, num2)
        self.assertEqual(correct_ans, karatsuba(num1, num2))
        self.assertEqual(correct_ans, fft(num1, num2))

    def test_large(self):
        num = [random.randrange(0, 2, 1) for k in range(2000)]
        correct_ans = reference_multiply(num, num)
        self.assertEqual(correct_ans, karatsuba(num, num))
        self.assertEqual(correct_ans, fft(num, num))

if __name__ == '__main__':
    unittest.main()