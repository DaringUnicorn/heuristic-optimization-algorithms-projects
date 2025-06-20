import collections
import random

def greedy_coloring(adj_list):
    """
    Colors a graph using a greedy algorithm with Largest Degree Ordering.

    Args:
        adj_list (dict): The adjacency list of the graph.

    Returns:
        tuple: A tuple containing:
            - int: The number of colors used.
            - dict: A dictionary mapping each vertex to its assigned color.
    """
    # Order vertices by degree (descending)
    nodes = sorted(adj_list.keys(), key=lambda v: len(adj_list[v]), reverse=True)

    colors = {}  # Stores color of each vertex

    for node in nodes:
        # Get colors of adjacent nodes
        neighbor_colors = {colors.get(neighbor) for neighbor in adj_list[node] if neighbor in colors}

        # Find the smallest available color
        current_color = 1
        while current_color in neighbor_colors:
            current_color += 1

        colors[node] = current_color

    # We need to make sure all nodes are colored, even disconnected ones
    all_nodes = set(adj_list.keys())
    colored_nodes = set(colors.keys())
    uncolored_nodes = all_nodes - colored_nodes
    for node in uncolored_nodes:
        colors[node] = 1 # Assign color 1 to disconnected nodes

    if not colors:
        return 0, {}
        
    num_colors = len(set(colors.values()))
    return num_colors, colors


def dsatur_coloring(adj_list):
    """
    Colors a graph using the DSatur algorithm.

    Args:
        adj_list (dict): The adjacency list of the graph.

    Returns:
        tuple: A tuple containing:
            - int: The number of colors used.
            - dict: A dictionary mapping each vertex to its assigned color.
    """
    nodes = set(adj_list.keys())
    if not nodes:
        return 0, {}

    colors = {}
    
    # Calculate initial degrees and saturation degrees
    degrees = {node: len(adj_list.get(node, [])) for node in nodes}
    saturation_degrees = {node: 0 for node in nodes}
    
    while len(colors) < len(nodes):
        uncolored_nodes = nodes - set(colors.keys())

        # Select the next node to color
        # Find the node with the maximum saturation degree.
        # Tie-break with the maximum degree.
        max_saturation = -1
        max_degree = -1
        next_node = None
        
        for node in uncolored_nodes:
            sat = saturation_degrees[node]
            deg = degrees[node]
            if sat > max_saturation:
                max_saturation = sat
                max_degree = deg
                next_node = node
            elif sat == max_saturation:
                if deg > max_degree:
                    max_degree = deg
                    next_node = node
        
        # If multiple nodes have the same saturation and degree, pick one
        if next_node is None:
            next_node = list(uncolored_nodes)[0]


        # Assign the smallest possible color
        neighbor_colors = {colors[neighbor] for neighbor in adj_list.get(next_node, []) if neighbor in colors}
        
        current_color = 1
        while current_color in neighbor_colors:
            current_color += 1
        colors[next_node] = current_color

        # Update saturation degrees of neighbors
        for neighbor in adj_list.get(next_node, []):
            if neighbor not in colors:
                # Check if the new color is a new color for the neighbor's neighborhood
                neighbor_neighbor_colors = {colors[nn] for nn in adj_list.get(neighbor, []) if nn in colors}
                if current_color not in neighbor_neighbor_colors:
                     saturation_degrees[neighbor] += 1
    
    num_colors = len(set(colors.values()))
    return num_colors, colors 

def welsh_powell_coloring(adj_list):
    """
    Colors a graph using the Welsh-Powell algorithm.
    
    Args:
        adj_list (dict): The adjacency list of the graph.
        
    Returns:
        tuple: A tuple containing:
            - int: The number of colors used.
            - dict: A dictionary mapping each vertex to its assigned color.
    """
    nodes = set(adj_list.keys())
    if not nodes:
        return 0, {}
    
    # Sort vertices by degree (descending)
    sorted_nodes = sorted(nodes, key=lambda v: len(adj_list.get(v, [])), reverse=True)
    
    colors = {}
    color_classes = []  # List of sets, each set contains vertices of the same color
    
    for node in sorted_nodes:
        if node in colors:
            continue
            
        # Find the first color class where this node can be placed
        placed = False
        for color_idx, color_class in enumerate(color_classes):
            # Check if node conflicts with any node in this color class
            conflicts = any(neighbor in color_class for neighbor in adj_list.get(node, []))
            if not conflicts:
                color_class.add(node)
                colors[node] = color_idx + 1
                placed = True
                break
        
        if not placed:
            # Create a new color class
            new_class = {node}
            color_classes.append(new_class)
            colors[node] = len(color_classes)
    
    num_colors = len(color_classes)
    return num_colors, colors

def smallest_last_coloring(adj_list):
    """
    Colors a graph using the Smallest-Last (SL) algorithm.
    """
    nodes = set(adj_list.keys())
    if not nodes:
        return 0, {}
    
    # Build degree dictionary
    degrees = {node: len(adj_list.get(node, [])) for node in nodes}
    remaining_nodes = set(nodes)
    ordering = []
    
    # Create ordering by repeatedly removing the node with smallest degree
    while remaining_nodes:
        min_node = min(remaining_nodes, key=lambda v: degrees[v])
        ordering.append(min_node)
        remaining_nodes.remove(min_node)
        
        # Update degrees of remaining neighbors
        for neighbor in adj_list.get(min_node, []):
            if neighbor in remaining_nodes:
                degrees[neighbor] -= 1
    
    # Color in reverse order
    colors = {}
    for node in reversed(ordering):
        neighbor_colors = {colors.get(neighbor) for neighbor in adj_list.get(node, []) if neighbor in colors}
        
        current_color = 1
        while current_color in neighbor_colors:
            current_color += 1
        colors[node] = current_color
    
    num_colors = len(set(colors.values())) if colors else 0
    return num_colors, colors

def random_ldo_coloring(adj_list, randomization_factor=0.3):
    """
    A randomized version of Largest Degree Ordering for diversity.
    """
    nodes = list(adj_list.keys())
    if not nodes:
        return 0, {}
    
    # Sort by degree but add some randomization
    node_degrees = [(node, len(adj_list.get(node, []))) for node in nodes]
    node_degrees.sort(key=lambda x: x[1], reverse=True)
    
    # Randomize the order slightly
    n = len(node_degrees)
    randomize_count = int(n * randomization_factor)
    
    for i in range(min(randomize_count, n-1)):
        if random.random() < 0.5:
            # Swap with next node
            node_degrees[i], node_degrees[i+1] = node_degrees[i+1], node_degrees[i]
    
    ordered_nodes = [node for node, _ in node_degrees]
    
    colors = {}
    for node in ordered_nodes:
        neighbor_colors = {colors.get(neighbor) for neighbor in adj_list.get(node, []) if neighbor in colors}
        
        current_color = 1
        while current_color in neighbor_colors:
            current_color += 1
        colors[node] = current_color
    
    num_colors = len(set(colors.values())) if colors else 0
    return num_colors, colors

def get_diverse_initial_solutions(adj_list, num_solutions=5):
    """
    Generate diverse initial solutions using different heuristics.
    """
    solutions = []
    
    # DSatur
    _, dsatur_sol = dsatur_coloring(adj_list)
    solutions.append(dsatur_sol)
    
    # Welsh-Powell
    _, wp_sol = welsh_powell_coloring(adj_list)
    solutions.append(wp_sol)
    
    # Smallest-Last
    _, sl_sol = smallest_last_coloring(adj_list)
    solutions.append(sl_sol)
    
    # Greedy LDO
    _, greedy_sol = greedy_coloring(adj_list)
    solutions.append(greedy_sol)
    
    # Random variations
    for _ in range(num_solutions - 4):
        _, random_sol = random_ldo_coloring(adj_list)
        solutions.append(random_sol)
    
    return solutions 
