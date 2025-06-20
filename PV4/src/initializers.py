import random

def dsatur_initializer(graph, num_colors):
    """
    DSATUR (Degree of Saturation) heuristic for graph coloring.
    Returns a coloring (chromosome) as a list of color assignments.
    """
    n = graph.num_vertices
    colors = [-1] * n
    saturation = [0] * n
    degrees = [len(graph.adj[v]) for v in range(n)]
    uncolored = set(range(n))

    while uncolored:
        # Select vertex with highest saturation, break ties by degree
        max_sat = max(saturation[v] for v in uncolored)
        candidates = [v for v in uncolored if saturation[v] == max_sat]
        if len(candidates) > 1:
            v = max(candidates, key=lambda x: degrees[x])
        else:
            v = candidates[0]
        # Assign the smallest available color
        neighbor_colors = set(colors[u] for u in graph.adj[v] if colors[u] != -1)
        for color in range(num_colors):
            if color not in neighbor_colors:
                colors[v] = color
                break
        # Update saturation of neighbors
        for u in graph.adj[v]:
            if colors[u] == -1:
                neighbor_colors_u = set(colors[w] for w in graph.adj[u] if colors[w] != -1)
                saturation[u] = len(neighbor_colors_u)
        uncolored.remove(v)
    return colors

def greedy_initializer(graph, num_colors):
    """
    Greedy coloring: Assigns the smallest possible color to each vertex in order.
    Returns a coloring (chromosome) as a list of color assignments.
    """
    n = graph.num_vertices
    colors = [-1] * n
    for v in range(n):
        neighbor_colors = set(colors[u] for u in graph.adj[v] if colors[u] != -1)
        for color in range(num_colors):
            if color not in neighbor_colors:
                colors[v] = color
                break
        if colors[v] == -1:
            # If no color is available, assign randomly (should not happen if num_colors is large enough)
            colors[v] = random.randint(0, num_colors - 1)
    return colors 
