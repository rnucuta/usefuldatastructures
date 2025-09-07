import unittest
from py_dsa.algorithms import name_node, thread_splitter, combiner_func, read_file
import os

class TestMapReduce(unittest.TestCase):
    def test_mr1(self):
        file_path = os.path.join(os.path.dirname(__file__), 'inputs', 'test_map_reduce.txt')
        data = read_file(file_path)
        n_threads = 8
        subsets = name_node(data, 1)
        reduced_count = thread_splitter(subsets)
        single_results = combiner_func(reduced_count)
        subsets = name_node(data, n_threads)
        reduced_count = thread_splitter(subsets)
        multi_results = combiner_func(reduced_count)
        self.assertEqual(single_results, multi_results)

if __name__ == '__main__':
    unittest.main()