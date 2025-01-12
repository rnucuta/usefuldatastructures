# https://leetcode.com/problems/valid-arrangement-of-pairs

from typing import List
from collections import defaultdict


def EularianPath(pairs: List[List[int]]) -> List[List[int]]:
    """Find a valid arrangement of pairs to form an Eulerian path.

    An Eulerian path is a path that visits every edge in a graph exactly once.
    In the context of this function, the input pairs represent edges in a graph,
    and the goal is to find an order in which these edges can be
    traversed such that each edge is visited exactly once. The requirements for
    a Eularian circuit on the other hand is a eularian path that ends at the
    start node. The requirements for it to be possible for this to exist is that
    at most one vertex has (outdegree - indegree) == 1 (start node), and one vertex has
    (indegree - outdegree) == 1 (end node), and the rest outdegree == indegree. Then, the
    eularian path, as shown in this problem, can be found by performing DFS
    with an edge visited set. This is an excellent source to learn more about the topic:
    https://www.youtube.com/watch?v=8MpoO2zA2l4

    Args:
        pairs (List[List[int]]): A list of pairs, where each pair represents an edge
            in the graph. Each pair is a list containing two integers, representing
            the nodes connected by the edge.

    Returns:
        List[List[int]]: A list of pairs in an order that forms a valid Eulerian path,
            if such a path exists. If no valid Eulerian path can be formed, an empty list
            is returned.

    """
    G = defaultdict(list)
    out_degree = defaultdict(int)
    in_degree = defaultdict(int)
    for u, v in pairs:
        G[u].append(v)
        out_degree[u] += 1
        in_degree[v] += 1

    starting_node = None
    for k in out_degree:
        if out_degree[k] - in_degree[k] == 1:
            starting_node = k
            break
        if not starting_node and out_degree[k] - in_degree[k] == -1:
            starting_node = k

    if starting_node is None:
        starting_node = pairs[0][0]

    result = []

    # algo is basically dfs
    # except you need to keep track
    # of visited edges not visited nodes
    def dfs(start: int) -> None:
        while G[start]:
            dfs(G[start].pop())
        if result:
            result.append([start, result[-1][0]])
        else:
            result.append([start, None])

    dfs(starting_node)

    result.reverse()
    result.pop()

    return result
