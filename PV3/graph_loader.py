import collections

def load_graph(file_path):
    """
    Loads a graph from a text file.

    The file format is expected to be:
    - First line: <number of vertices> <number of edges>
    - Subsequent lines: <vertex_u> <vertex_v>

    Args:
        file_path (str): The path to the graph file.

    Returns:
        tuple: A tuple containing:
            - int: The number of vertices.
            - int: The number of edges.
            - dict: The adjacency list representation of the graph.
    """
    adj_list = collections.defaultdict(list)
    with open(file_path, 'r') as f:
        try:
            first_line = f.readline().strip().split()
            if len(first_line) < 2:
                raise ValueError("Invalid file format: First line should contain number of vertices and edges.")
            num_vertices, num_edges = int(first_line[0]), int(first_line[1])

            for line in f:
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                u, v = map(int, parts)
                adj_list[u].append(v)
                adj_list[v].append(u)
        except (IOError, ValueError) as e:
            print(f"Error reading file {file_path}: {e}")
            return 0, 0, None

    return num_vertices, num_edges, adj_list 
