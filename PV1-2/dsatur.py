import sys
from collections import defaultdict

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = [set() for _ in range(n)]
    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            n, m = map(int, f.readline().split())
            G = cls(n)
            for line in f:
                u, v = map(int, line.split())
                G.adj[u].add(v)
                G.adj[v].add(u)
        return G

def greedy_dsatur(G):
    n = G.n
    colors = [-1]*n
    neighbor_colors = [set() for _ in range(n)]
    degrees = [len(G.adj[u]) for u in range(n)]
    for _ in range(n):
        # pick uncolored vertex with max saturation, tie by degree
        sat_deg = [ (len(neighbor_colors[u]), degrees[u], u)
                    for u in range(n) if colors[u]==-1 ]
        _, _, u = max(sat_deg)
        # assign the smallest available color
        used = neighbor_colors[u]
        for c in range(n):
            if c not in used:
                colors[u] = c
                break
        # update neighbors' saturation info
        for v in G.adj[u]:
            if c not in neighbor_colors[v]:
                neighbor_colors[v].add(c)
    num_colors = max(colors) + 1
    return colors, num_colors

def dsatur_exact(G, time_limit=None):
    sys.setrecursionlimit(10000)
    n = G.n
    # initial upper bound
    best_colors, best_k = greedy_dsatur(G)

    # structures for recursive search
    colors = [-1]*n
    neighbor_colors = [set() for _ in range(n)]
    degrees = [len(G.adj[u]) for u in range(n)]

    def search(colored_cnt, used_k):
        nonlocal best_k, best_colors

        # prune on color-count
        if used_k >= best_k:
            return
        # if all colored, we've found a better solution
        if colored_cnt == n:
            best_k = used_k
            best_colors = colors.copy()
            return

        # pick next vertex: max saturation, tie by degree
        sat_deg = [ (len(neighbor_colors[u]), degrees[u], u)
                    for u in range(n) if colors[u]==-1 ]
        _, _, u = max(sat_deg)

        forbidden = neighbor_colors[u]
        # try existing colors
        for c in range(used_k):
            if c not in forbidden:
                colors[u] = c
                # update neighbor info
                updated = []
                for v in G.adj[u]:
                    if colors[v]==-1 and c not in neighbor_colors[v]:
                        neighbor_colors[v].add(c)
                        updated.append(v)
                search(colored_cnt+1, used_k)
                # backtrack
                colors[u] = -1
                for v in updated:
                    neighbor_colors[v].remove(c)
        # try a new color
        colors[u] = used_k
        updated = []
        for v in G.adj[u]:
            if colors[v]==-1:
                neighbor_colors[v].add(used_k)
                updated.append(v)
        search(colored_cnt+1, used_k+1)
        colors[u] = -1
        for v in updated:
            neighbor_colors[v].remove(used_k)

    search(colored_cnt=0, used_k=0)
    return best_colors, best_k

if __name__ == "__main__":
    import argparse, time
    p = argparse.ArgumentParser(description="Greedy DSATUR graph-coloring")
    p.add_argument("input", help="path to graph file")
    args = p.parse_args()

    G = Graph.from_file(args.input)
    t0 = time.time()
    coloring, k = greedy_dsatur(G)
    t1 = time.time()
    print(f"Found coloring with {k} colors in {t1-t0:.2f}s")
    # No longer printing the color of each vertex
