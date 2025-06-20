def read_graph(path: str) -> dict[int, list[int]]:
    """
    Read an undirected graph from the given file.
    Args:
        path: path to the .txt file containing edge-list.
    Returns:
        adjacency_list: dict mapping node->list of neighbor nodes
    """
    adjacency_list = {}
    
    with open(path, 'r') as f:
        # Read first line to get number of nodes and edges
        num_nodes, num_edges = map(int, f.readline().split())
        
        # Initialize adjacency list with empty lists for each node
        for i in range(num_nodes):
            adjacency_list[i] = []
            
        # Read edges and build adjacency list
        for _ in range(num_edges):
            u, v = map(int, f.readline().split())
            # Add edge in both directions since graph is undirected
            adjacency_list[u].append(v)
            adjacency_list[v].append(u)
            
    return adjacency_list

if __name__ == "__main__":
    # örnek: gc_50_9.txt dosyasını oku ve ilk birkaç komşuyu göster
    G = read_graph("gc_50_9.txt")
    print(f"Total nodes: {len(G)}")
    print("Neighbors of node 0:", G.get(0))
    # Beklenti: G bir dict, G[0] komşu listesini içermeli 