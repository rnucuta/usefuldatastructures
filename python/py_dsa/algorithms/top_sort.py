from collections import defaultdict, deque
from typing import List, Any
from py_dsa.datastructures import Graph


# Khan's algorithm
# returns list of nodes if valid
# otherwise empty list
def topological_sort(G: Graph) -> List[Any]:
    """Perform topological sorting on a directed graph.

    Args:
        G (Graph): The graph to be sorted.

    Returns:
        List[Any]: A list of nodes in topologically sorted order if the graph is acyclic,
                    otherwise an empty list.

    """
    n = G.num_nodes()
    indegree = [0] * n
    for u in G.get_nodes():
        for v in G.get_edges(u):
            indegree[G.get_idx(v)] += 1

    dq = deque()

    for i in range(n):
        if not indegree[i]:
            dq.append(i)

    top_sorted_idxs = []
    while dq:
        u_idx = dq.popleft()
        top_sorted_idxs.append(u_idx)

        u_val = G.get_nodes()[u_idx]
        for v_val in G.get_edges(u_val):
            v_idx = G.get_idx(v_val)
            indegree[v_idx] -= 1

            if not indegree[v_idx]:
                dq.append(v_idx)

    # Check for cycle
    if len(top_sorted_idxs) != n:
        return []
    return [G.get_nodes()[idx] for idx in top_sorted_idxs]


# detect cycle in undirected graph
# TODO: add support for graph class
def validTree(n: int, edges: List[List[int]]) -> bool:
    """Determine if the given edges form a valid tree.

    Args:
        n (int): The number of nodes.
        edges (List[List[int]]): The edges of the graph.

    Returns:
        bool: True if the edges form a valid tree, False otherwise.

    """
    visited = set()
    G = defaultdict(set)
    for a, b in edges:
        G[a].add(b)
        G[b].add(a)

    def dfs(u: int, parent: int) -> bool:
        # print(u, parent)
        visited.add(u)
        for v in G[u]:
            if v not in visited:
                if not dfs(v, u):
                    # print(v, u)
                    return False
            # cycle detected
            # if you have visited a node already
            # in your adjacency list that isnt your
            # parent, then at some point another branch of
            # dfs has visited that point
            # meaning that there is a cycle
            elif v != parent:
                return False

        return True

    if dfs(0, None):
        # print(len(visited))
        return len(visited) == n
    return False


# TODO: add support for graph class
def is_bipartite(g_l: dict) -> bool:
    """Test if a given graph is bipartite using BFS.

    Args:
        g_l (dict): A dictionary of adjacency lists representing the graph.

    Returns:
        bool: True if the graph is bipartite, False otherwise.

    """
    node_colors = {k: None for k in g_l}
    # perform BFS for each connected component
    for starting_node in g_l:
        if node_colors[starting_node] is not None:
            continue
        # see if any neighbor is already set to try to set the color
        # correctly initially
        if g_l[starting_node]:
            for neighbor in g_l[starting_node]:
                if node_colors[neighbor] is not None:
                    node_colors[starting_node] = node_colors[neighbor] ^ 1
                    break
        # if still not set, then set it to color 0
        if node_colors[starting_node] is None:
            node_colors[starting_node] = 0
        queue = deque([starting_node])
        # BFS to check if the graph is bipartite
        # dont need to check for visited nodes
        # as they are being colored
        while queue:
            node = queue.popleft()
            for neighbor in g_l[node]:
                if node_colors[neighbor] is None:
                    node_colors[neighbor] = node_colors[node] ^ 1
                    queue.append(neighbor)
                elif node_colors[neighbor] == node_colors[node]:
                    return False
    return True


# TODO: add strongly connected components
