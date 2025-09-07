import unittest
from py_dsa.datastructures.lfu_cache import LFUCache

class TestLFUCache(unittest.TestCase):
    def test_leetcode_case(self):
        lfu = LFUCache(2)
        lfu.put(1, 1)
        lfu.put(2, 2)
        self.assertEqual(lfu.get(1), 1)
        lfu.put(3, 3)
        self.assertRaises(KeyError, lfu.get, 2)
        self.assertEqual(lfu.get(3), 3)
        lfu.put(4, 4)
        self.assertRaises(KeyError, lfu.get, 1)
        self.assertEqual(lfu.get(3), 3)
        self.assertEqual(lfu.get(4), 4)

if __name__ == "__main__":
    unittest.main()
