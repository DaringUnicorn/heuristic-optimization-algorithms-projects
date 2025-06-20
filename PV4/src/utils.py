from graph import Graph

def parse_dimacs_graph(file_path):
    """
    Parses a graph from a file in the format used by the data files.
    
    Args:
        file_path (str): The path to the graph file.

    Returns:
        Graph: A Graph object representing the parsed graph.
    """
    edges = []
    num_vertices = 0
    num_edges = 0

    with open(file_path, 'r') as f:
        # First line contains: num_vertices num_edges
        first_line = f.readline().strip()
        parts = first_line.split()
        num_vertices = int(parts[0])
        num_edges = int(parts[1])
        
        # Read edges
        for line in f:
            if line.strip():  # Skip empty lines
                parts = line.strip().split()
                u = int(parts[0])
                v = int(parts[1])
                edges.append((u, v))
    
    if num_vertices == 0 or num_edges == 0:
        raise ValueError("Failed to parse graph file.")

    return Graph(num_vertices, num_edges, edges) 
