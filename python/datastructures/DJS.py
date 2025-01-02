class DisjointSet:
    def __init__(self, start_size, start_keys):
        assert start_size >= 0
        assert len(start_keys) == start_size

        self.parent = [0] * (start_size + 1)
        self.idx_key_map = [None] + [k for k in start_keys]
        self.key_idx_map = {k : i + 1 for i, k in enumerate(start_keys)}
        self._num_djsets = start_size

    def add_key(self, key):
        assert key not in self.key_idx_map

        self.key_idx_map[key] = len(self.parent)
        self.parent.append(0)
        self.idx_key_map.append(key)
        self._num_djsets += 1

    def find_set(self, u):
        u_parent_idx = self._find_set(self.key_idx_map[u])
        return self.idx_key_map[u_parent_idx] 
    
    def _find_set(self, u):
        if self.parent[u] <= 0:
            return u
        self.parent[u] = self.find_set(self.parent[u])
        return self.parent[u]

    def link(self, u, v):
        idx_u = self.key_idx_map[u]
        idx_v = self.key_idx_map[v]
        
        assert self.parent[idx_u] <= 0 and self.parent[idx_v] <= 0, \
            "Can only link parents of djsets, use find_set first to get parent"

        if self.parent[idx_u] < self.parent[idx_v]:
            self.parent[idx_v] = idx_u
        else:
            if self.parent[idx_u] == self.parent[idx_v]:
                self.parent[idx_v] -= 1
            self.parent[idx_u] = idx_v

        self._num_djsets -= 1

    def union(self, u, v):
        parent_u, parent_v = self.find_set(u), self.find_set(v)
        if parent_u != parent_v:
            self.link(parent_u, parent_v)
            return True
        return False    

    def get_num_djsets(self):
        return self._num_djsets