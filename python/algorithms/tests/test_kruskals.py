import unittest
import sys
sys.path.append("..")

from kruskals import MST

def cookies_distrubution_map(apartments) -> list:
    # create all nodes
    home_node_idx = n = len(apartments)
    home_node = ((n+1)//2, (n+1)//2)
    apartments.append(home_node)

    graph = MST(n+1)

    # add nodes to graph
    for i, node in enumerate(apartments):
        for j, node_p in enumerate(apartments[i+1:]):
            # compute manhattan distance
            manhattan_d = abs(node[0]-node_p[0])+abs(node[1]-node_p[1])
            graph.add_edge(i, j+i+1, manhattan_d, node, node_p)
    
    # print(graph.edges)

    #kruskal
    graph.kruskal()
    # n is index of home node
    # breadth-first search for spanning tree starting at home node
    # we have same number of nodes, and n-1 edges, so don't need to construct new graph
    # instead of traversing whole tree, traverse mst saved from kruskal
    # print(graph.bfs_with_map(home_node_idx))
    res = graph.bfs_with_map(home_node_idx)
    apartments.pop()
    return res

class TestProblem5(unittest.TestCase):
    ### Public tests
    def test_correctness_public_n2_split(self):
        route = MST([(1,2), (2, 1)])
        self.assertEqual({((1,1), (1,2)), ((1,1), (2,1))}, set(route))

    def test_correctness_public_n2_sequential(self):
        route = MST([(1,2), (1, 5)])
        self.assertEqual({((1,1), (1,2)), ((1,2), (1,5))}, set(route))

    def test_correctness_public_n3_tie(self):
        route = MST([(1, 1), (1,2), (2, 1)])
        self.assertEqual({((2, 2), (1, 2)), ((1, 2), (1, 1)), ((1, 1), (2, 1))}, set(route))

    def test_correctness_public_n4_sequential(self):
        route = MST([(1, 1), (3, 3), (4, 4), (5, 5)])
        self.assertEqual({((2, 2), (1, 1)), ((2, 2), (3, 3)), ((3, 3), (4, 4)), ((4, 4), (5, 5))}, set(route))

    def test_correctness_public_n4_split(self):
        route = MST([(1, 5), (2, 5), (1, 7), (6, 1)])
        self.assertEqual({((2, 2), (2, 5)), ((2, 5), (1, 5)), ((1, 5), (1, 7)), ((2, 2), (6, 1))}, set(route))

    def test_correctess_public_n6(self):
        route = MST([(1,4), (5, 1), (5, 5), (5, 4), (3, 2), (6, 4)])
        self.assertTrue({((3, 3), (3, 2)), ((3, 2), (5, 1)), ((3, 3), (1, 4)), ((5, 1), (5, 4)), ((5, 4), (5, 5)), ((5, 4), (6, 4))} == set(route) \
            or {((3, 3), (3, 2)), ((3, 2), (5, 1)), ((3, 3), (1, 4)), ((3, 3), (5, 4)), ((5, 4), (5, 5)), ((5, 4), (6, 4))} == set(route))
        
if __name__ == '__main__':
    unittest.main()