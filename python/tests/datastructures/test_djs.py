import unittest
from py_dsa.datastructures.djs import DisjointSet

class TestDisjointSet(unittest.TestCase):
    def test_initialization_and_find(self):
        ds = DisjointSet(3, ['a', 'b', 'c'])
        self.assertEqual(ds.find_set('a'), 'a')
        self.assertEqual(ds.find_set('b'), 'b')
        self.assertEqual(ds.find_set('c'), 'c')
        self.assertEqual(ds.get_num_djsets(), 3)

    def test_add_key(self):
        ds = DisjointSet(2, ['x', 'y'])
        ds.add_key('z')
        self.assertEqual(ds.find_set('z'), 'z')
        self.assertEqual(ds.get_num_djsets(), 3)
        with self.assertRaises(AssertionError):
            ds.add_key('x')  # Already exists

    def test_union_and_find(self):
        ds = DisjointSet(4, [1, 2, 3, 4])
        self.assertTrue(ds.union(1, 2))
        self.assertEqual(ds.find_set(1), ds.find_set(2))
        self.assertEqual(ds.get_num_djsets(), 3)
        self.assertTrue(ds.union(3, 4))
        self.assertEqual(ds.find_set(3), ds.find_set(4))
        self.assertEqual(ds.get_num_djsets(), 2)
        # Union two sets
        self.assertTrue(ds.union(1, 3))
        self.assertEqual(ds.find_set(1), ds.find_set(3))
        self.assertEqual(ds.get_num_djsets(), 1)
        # Union already united sets
        self.assertFalse(ds.union(2, 4))
        self.assertEqual(ds.get_num_djsets(), 1)

    def test_path_compression(self):
        ds = DisjointSet(5, list('abcde'))
        ds.union('a', 'b')
        ds.union('b', 'c')
        ds.union('c', 'd')
        # All should have the same representative
        rep = ds.find_set('a')
        for k in 'bcde':
            self.assertEqual(ds.find_set(k), rep)
        self.assertEqual(ds.get_num_djsets(), 2)  # 'e' is still separate

    def test_mixed_types(self):
        ds = DisjointSet(2, [42, 'foo'])
        ds.add_key((1, 2))
        self.assertEqual(ds.get_num_djsets(), 3)
        ds.union(42, (1, 2))
        self.assertEqual(ds.get_num_djsets(), 2)
        self.assertEqual(ds.find_set(42), ds.find_set((1, 2)))

if __name__ == "__main__":
    unittest.main()