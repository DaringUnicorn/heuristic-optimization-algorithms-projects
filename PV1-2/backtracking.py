def color_backtrack(G: dict[int, list[int]], k: int) -> dict[int, int] | None:
    """
    Recursive backtracking graph coloring.
    """
    def is_safe(node: int, color: int, coloring: dict[int, int]) -> bool:
        """Check if it's safe to color 'node' with 'color' given current 'coloring'"""
        for neighbor in G[node]:
            if neighbor in coloring and coloring[neighbor] == color:
                return False
        return True

    def backtrack(node: int, coloring: dict[int, int]) -> dict[int, int] | None:
        """Recursive backtracking helper function"""
        # Base case: all nodes are colored
        if node == len(G):
            return coloring.copy()
        
        # Try each color for current node
        for color in range(k):
            if is_safe(node, color, coloring):
                # Try this color
                coloring[node] = color
                
                # Recursively color remaining nodes
                result = backtrack(node + 1, coloring)
                if result is not None:
                    return result
                
                # Backtrack: remove this color assignment
                coloring.pop(node)
        
        # No valid coloring found for this branch
        return None

    # Start with empty coloring and node 0
    return backtrack(0, {})

if __name__ == "__main__":
    from parser import read_graph
    from backtracking import color_backtrack

    G = read_graph("tiny.txt")
    solution = color_backtrack(G, 9)
    if solution:
        print("Found coloring with 9 colors:", solution)
    else:
        print("No valid coloring found with 9 colors.") 