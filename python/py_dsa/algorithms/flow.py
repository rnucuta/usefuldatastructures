from collections import deque
from py_dsa.datastructures import MatchingGraph
from typing import List


class MaxFlow:
    def __init__(self, MG: MatchingGraph):
        self.MG = MG

    def find_path(self) -> List[int]:
        """Find a simple path from source to sink using BFS.

        Returns:
            List[int]: A list of vertices representing the path from source to sink, or None if no path exists.

        """
        # find a simple path from s to t
        # using bfs
        # visited = [False]*len(G)
        visited = set()
        # parent = [-1]*len(G)
        parent = {}
        queue = deque([self.MG.get_source()])
        # visited[s] = True
        visited.add(self.MG.get_source())

        while queue:
            u = queue.popleft()
            # push forward on edges with excess capacity
            for v in self.MG.get_edges(u):
                if v == u or not self.MG.edge_exists(u, v):
                    continue
                residual = self.MG.get_edge_weight(
                    u, v
                ) - self.MG.get_residual_edge_weight(u, v)
                if v not in visited and residual > 0:
                    queue.append(v)
                    # visited[v] = True
                    visited.add(v)
                    parent[v] = u
                    if v == self.MG.get_sink():
                        return self.reconstruct_path(parent)
            # push backwards on edges already carrying flow (positive)
            # to u (current node) in residual graph (so really u to v
            # in real graph) to opposite direction
            # In other words, allows us to redirect flow that might
            # have been sent on a suboptimal path
            for v in self.MG.get_residual_nodes():
                if (
                    not v == u
                    and v not in visited
                    and self.MG.residual_edge_exists(v, u)
                    and self.MG.get_residual_edge_weight(v, u) > 0
                ):
                    # print(u, v)
                    queue.append(v)
                    # visited[v] = True
                    visited.add(v)
                    parent[v] = u  # swap parent
                    if v == self.MG.get_sink():
                        return self.reconstruct_path(parent)
        return None

    # get path from BFS by traversing through parents array
    def reconstruct_path(self, parent: List[int]) -> List[int]:
        """Reconstruct the path from source to sink using the parent mapping.

        Args:
            parent (List[int]): The parent mapping from BFS.

        Returns:
            List[int]: The reconstructed path from source to sink.

        """
        path = []
        v = self.MG.get_sink()
        while v != self.MG.get_source():
            u = parent[v]
            path.append((u, v))
            v = u
        path.reverse()
        return path

    def bottleneck(self, path: List[int]) -> int:
        """Find the minimum residual capacity of any edge on the given path.

        Args:
            path (List[int]): A simple path from source to sink.

        Returns:
            int: The bottleneck capacity of the path.

        """
        # min residual capacity of any edge on path
        # path is a simple path from s to t
        b = float("inf")
        for u, v in path:
            if self.MG.edge_exists(u, v):  # Forward edge
                b = min(
                    b,
                    self.MG.get_edge_weight(u, v)
                    - self.MG.get_residual_edge_weight(u, v),
                )
            else:  # Backward edge
                b = min(b, self.MG.get_residual_edge_weight(v, u))
        # if b < 0:
        #     print(b)
        return b

    # update residual graph with bottleneck
    def augment(self, path: List[int], b: int) -> None:
        """Augment the flow along the given path by the bottleneck value.

        Args:
            path (List[int]): The path along which to augment flow.
            b (int): The bottleneck value to augment by.

        """
        # print(path)
        # augment flow along path by b
        for u, v in path:
            F_uv = self.MG.get_residual_edge_weight(u, v)
            if self.MG.edge_exists(u, v):  # Forward edge
                self.MG.update_residual_edge_weight(u, v, F_uv + b)
            else:  # Backward edge
                # print(u, v)
                # print(F[v][u])
                self.MG.update_residual_edge_weight(u, v, F_uv - b)

    def max_flow_val(self) -> int:
        """Calculate the maximum flow value from source to sink.

        Returns:
            int: The maximum flow value.

        """
        path = self.find_path()
        # i = 0
        while path:
            # if i == 5:
            #     break
            # print("step",  i)
            # i += 1
            b = self.bottleneck(path)
            # print("b", b, "i", i)
            self.augment(path, b)
            new_path = self.find_path()
            if path == new_path:
                break
            path = new_path

        max_flow_value = sum(
            self.MG.get_residual_edge_weight(self.MG.get_source(), v)
            for v in self.MG.get_edges(self.MG.get_source())
        )
        return max_flow_value
