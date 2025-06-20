import collections

class Graph:
    """
    Represents a graph using an adjacency list.
    """
    def __init__(self, num_vertices, num_edges, edges):
        self.num_vertices = num_vertices
        self.num_edges = num_edges
        self.adj = collections.defaultdict(set)
        for u, v in edges:
            # DIMACS nodes are 1-indexed, we use 0-indexed
            self.adj[u - 1].add(v - 1)
            self.adj[v - 1].add(u - 1)

    def __str__(self):
        return f"Graph with {self.num_vertices} vertices and {self.num_edges} edges." 
