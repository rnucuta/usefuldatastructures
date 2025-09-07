# TODO: fix typing
# TODO: use djs class

from collections import defaultdict, deque
# from py_dsa.datastructures import DisjointSet


class MST:
    """Minimum Spanning Tree"""

    def __init__(self, nodes: int):
        """Initialize the MST with a given number of nodes."""
        self.num_nodes = nodes
        self.node_map = {}
        self.edges = []
        self.mst = None

    def add_edge(self, u: int, v: int, w: int, n_u: any, n_v: any) -> None:
        """Add an edge to the MST with specified nodes and weight."""
        self.edges.append([u, v, w])
        # save nodes for later bfs traversal output
        if n_u not in self.node_map:
            self.node_map[u] = n_u
        if n_v not in self.node_map:
            self.node_map[v] = n_v

    # disjoint sets operations
    def find_set(self, parent: list[int], u: int) -> int:
        """Find the representative of the set that contains u."""
        if parent[u] <= 0:
            return u
        else:
            parent[u] = self.find_set(parent, parent[u])
            return parent[u]

    def link(self, parent: list[int], u: int, v: int) -> None:
        """Link two sets with roots u and v."""
        if -parent[u] > -parent[v]:
            parent[v] = u
        else:
            if -parent[u] == parent[v]:
                parent[v] = parent[v] - 1
            parent[u] = v

    # takes root, or result of find set, as input
    # to avoid redundant find set calls
    def union(self, parent: list[int], fs_u: int, fs_v: int) -> None:
        """Union the sets containing fs_u and fs_v."""
        self.link(parent, fs_u, fs_v)

    # algorithm is same as connected components, except stops when
    # n-1 is reached. Conveniently, our graph will be fully connected
    def kruskal(self) -> list[list[int]]:
        """Execute Kruskal's algorithm to find the Minimum Spanning Tree."""
        result = []
        i = 0  # index of edge we are currently looking at
        e = 0  # edge counter

        # sort edges in ascending order by weight
        self.edges = sorted(self.edges, key=lambda edge: edge[2])

        parent = []

        # create disjoint-sets for all vertices where they are their own
        # parent initially
        for _ in range(self.num_nodes):
            parent.append(0)

        # Number of edges to be taken is less than to nodes-1
        while e < self.num_nodes - 1:
            # Pick the smallest edge and increment
            # the index for next iteration
            # print(result)
            u, v, w = self.edges[i]
            i = i + 1
            root_u = self.find_set(parent, u)
            root_v = self.find_set(parent, v)

            # If including this edge doesn't
            # cause cycle (x and y dont share a common parent), include it
            if root_u != root_v:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, root_u, root_v)

        self.mst = result
        return result

    def bfs_with_map(self, home: int) -> list[tuple[any, any]]:
        """Perform BFS traversal from the given home node, returning mapped node values."""
        # return final output with indices of nodes
        # mapped to their actual values
        if self.mst is None:
            return []

        result = []
        visited = set()
        queue = deque([home])
        visited.add(home)
        # print(home)

        # do not have adjacency list. if were to just iterate over edges
        # would have to time complexity of O(nxe), which is O(n*(n-1)/2) = 0(n^2)
        # with adjacency list rep, tc is O(n+e), so will assemble adjacency list first
        adjacency_list = defaultdict(set)
        for edge in self.mst:
            u, v, _ = edge
            adjacency_list[u].add(v)
            adjacency_list[v].add(u)

        # print(adjacency_list)

        while queue:
            u = queue.popleft()
            for v in adjacency_list[u]:
                if v not in visited:
                    queue.append(v)
                    visited.add(v)
                    result.append((self.node_map[u], self.node_map[v]))

        return result
