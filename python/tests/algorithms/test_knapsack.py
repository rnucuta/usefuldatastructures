import unittest
import sys
sys.path.append("..")

from py_dsa.algorithms.knapsack import find_max_form


class TestKnapsack(unittest.TestCase):
  def test_correctness_public_a1(self):
    """Public test """
    strs = ["10","0001","111001","1","0"]
    m = 5
    n = 3
    self.assertEqual(find_max_form(strs, m, n), 4)

  def test_correctness_public_a2(self):
    """Public test """
    strs = ["10","0","1"]
    m = 1
    n = 1
    self.assertEqual(find_max_form(strs, m, n), 2)

  def test_correctness_public_a3(self):
    """Public test """
    strs = ['10000',
      '0110011',
      '01010110',
      '100101010',
      '101',
      '100011',
      '100010010',
      '000001',
      '11011',
      '01111',
      '101011',
      '0000100',
      '11000110',
      '0011001',
      '011000110',
      '11010110',
      '101001',
      '001',
      '110011011',
      '000111',
      '10110',
      '11000',
      '01001',
      '10001',
      '100',
      '000111110',
      '110',
      '001',
      '00110101',
      '01011001',
      '101',
      '001010100',
      '01001011',
      '1010',
      '0001101',
      '001',
      '01001',
      '011000',
      '10001',
      '0101',
      '10001000',
      '11100101',
      '00111',
      '110011001',
      '1110011',
      '1000110',
      '111011010',
      '0010111',
      '000',
      '0101']
    m = 40
    n = 50
    self.assertEqual(find_max_form(strs, m, n), 20)


if __name__ == '__main__':
  unittest.main()
