def greedy_coloring(G: dict[int, list[int]], order: list[int] | None = None) -> dict[int, int]:
    """
    Simple greedy graph coloring.
    If order is None, nodes are processed in descending degree order.
    Otherwise, uses the provided node order.
    """
    # If no order provided, sort nodes by degree (descending)
    if order is None:
        order = sorted(G.keys(), key=lambda x: len(G[x]), reverse=True)
    
    # Initialize coloring and available colors for each node
    coloring = {}
    
    # Process nodes in the given order
    for node in order:
        # Find the smallest available color
        used_colors = {coloring[neighbor] for neighbor in G[node] if neighbor in coloring}
        color = 0
        while color in used_colors:
            color += 1
        coloring[node] = color
    
    return coloring

def dsatur_coloring(G: dict[int, list[int]]) -> dict[int, int]:
    """
    DSATUR graph coloring algorithm.
    At each step, picks the node with highest saturation (number of distinct neighbor colors).
    Ties are broken by degree.
    """
    # Initialize data structures
    coloring = {}
    saturation = {node: 0 for node in G}  # Number of distinct colors in neighborhood
    uncolored = set(G.keys())
    
    while uncolored:
        # Find node with maximum saturation
        max_sat = max(saturation[node] for node in uncolored)
        candidates = [node for node in uncolored if saturation[node] == max_sat]
        
        # Break ties by degree
        node = max(candidates, key=lambda x: len(G[x]))
        
        # Find smallest available color
        used_colors = {coloring[neighbor] for neighbor in G[node] if neighbor in coloring}
        color = 0
        while color in used_colors:
            color += 1
        
        # Color the node
        coloring[node] = color
        uncolored.remove(node)
        
        # Update saturation for neighbors
        for neighbor in G[node]:
            if neighbor in uncolored:
                neighbor_colors = {coloring[n] for n in G[neighbor] if n in coloring}
                saturation[neighbor] = len(neighbor_colors)
    
    return coloring

if __name__ == "__main__":
    from parser import read_graph
    
    # Test both algorithms
    G = read_graph("gc_50_9.txt")
    
    # Test simple greedy
    greedy_solution = greedy_coloring(G)
    print("Simple greedy coloring:")
    print(f"Number of colors used: {max(greedy_solution.values()) + 1}")
    print("Sample coloring:", dict(sorted(greedy_solution.items())[:5]))
    
    # Test DSATUR
    dsatur_solution = dsatur_coloring(G)
    print("\nDSATUR coloring:")
    print(f"Number of colors used: {max(dsatur_solution.values()) + 1}")
    print("Sample coloring:", dict(sorted(dsatur_solution.items())[:5])) 