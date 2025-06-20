#!/usr/bin/env python3
"""
GRAPH ANALYSIS: Check graph properties and structure
"""

from graph_loader import load_graph
import collections

def analyze_graph():
    """Comprehensive graph analysis"""
    
    print("🔬 COMPREHENSIVE GRAPH ANALYSIS")
    print("=" * 50)
    
    # Load graph
    num_vertices, num_edges, graph = load_graph('gc_50_9.txt')
    
    print(f"📊 BASIC STATS:")
    print(f"   Vertices: {num_vertices}")
    print(f"   Edges: {num_edges}")
    print(f"   Max possible edges: {num_vertices * (num_vertices-1) // 2}")
    print(f"   Edge density: {num_edges / (num_vertices * (num_vertices-1) // 2) * 100:.1f}%")
    
    # Check vertex degrees
    degrees = []
    for v in range(num_vertices):
        degree = len(graph.get(v, []))
        degrees.append(degree)
    
    print(f"\n🎯 DEGREE ANALYSIS:")
    print(f"   Min degree: {min(degrees)}")
    print(f"   Max degree: {max(degrees)}")
    print(f"   Avg degree: {sum(degrees) / len(degrees):.1f}")
    print(f"   Max possible degree: {num_vertices - 1}")
    
    # Check degree distribution
    degree_counts = collections.Counter(degrees)
    print(f"\n📈 DEGREE DISTRIBUTION:")
    for degree in sorted(degree_counts.keys()):
        count = degree_counts[degree]
        print(f"   Degree {degree:2d}: {count:2d} vertices")
    
    # Check for unusual patterns
    print(f"\n🔍 STRUCTURE ANALYSIS:")
    
    # Check if graph is symmetric
    symmetric = True
    for u in graph:
        for v in graph[u]:
            if u not in graph.get(v, []):
                symmetric = False
                print(f"   ⚠️  Asymmetric edge: {u}->{v} but not {v}->{u}")
                break
        if not symmetric:
            break
    
    if symmetric:
        print(f"   ✅ Graph is symmetric (undirected)")
    
    # Check for self-loops
    self_loops = 0
    for v in graph:
        if v in graph[v]:
            self_loops += 1
            print(f"   ⚠️  Self-loop at vertex {v}")
    
    if self_loops == 0:
        print(f"   ✅ No self-loops found")
    
    # Check edge count consistency
    total_directed_edges = sum(len(neighbors) for neighbors in graph.values())
    expected_directed = num_edges * 2  # Each undirected edge = 2 directed
    
    print(f"\n📊 EDGE COUNT VERIFICATION:")
    print(f"   Reported edges: {num_edges}")
    print(f"   Directed edges in adjacency list: {total_directed_edges}")
    print(f"   Expected directed (if undirected): {expected_directed}")
    print(f"   Match: {total_directed_edges == expected_directed}")
    
    # Check for suspicious patterns that might make coloring easy
    print(f"\n🕵️ SUSPICIOUS PATTERN CHECK:")
    
    # Check for cliques (complete subgraphs)
    max_clique_size = 0
    for v in range(num_vertices):
        neighbors = set(graph.get(v, []))
        clique_size = 1  # vertex itself
        
        # Check how many neighbors are connected to each other
        for n1 in neighbors:
            all_connected = True
            for n2 in neighbors:
                if n1 != n2 and n2 not in graph.get(n1, []):
                    all_connected = False
                    break
            if all_connected:
                clique_size = len(neighbors) + 1
                break
        
        max_clique_size = max(max_clique_size, clique_size)
    
    print(f"   Estimated max clique size: {max_clique_size}")
    
    # Check for bipartite structure
    # Try 2-coloring with BFS
    colors = {}
    is_bipartite = True
    
    def bfs_2_color(start):
        queue = [start]
        colors[start] = 0
        
        while queue:
            vertex = queue.pop(0)
            vertex_color = colors[vertex]
            
            for neighbor in graph.get(vertex, []):
                if neighbor in colors:
                    if colors[neighbor] == vertex_color:
                        return False  # Not bipartite
                else:
                    colors[neighbor] = 1 - vertex_color
                    queue.append(neighbor)
        return True
    
    for v in range(num_vertices):
        if v not in colors:
            if not bfs_2_color(v):
                is_bipartite = False
                break
    
    if is_bipartite:
        print(f"   🚨 GRAPH IS BIPARTITE! (2-colorable)")
        print(f"       This explains why coloring is so easy!")
        color_count = collections.Counter(colors.values())
        print(f"       Partition sizes: {dict(color_count)}")
    else:
        print(f"   ✅ Graph is not bipartite")
    
    # Check connectivity
    visited = set()
    components = 0
    
    def dfs(v):
        if v in visited:
            return
        visited.add(v)
        for neighbor in graph.get(v, []):
            dfs(neighbor)
    
    for v in range(num_vertices):
        if v not in visited:
            components += 1
            dfs(v)
    
    print(f"   Connected components: {components}")
    
    return is_bipartite, max_clique_size, components

if __name__ == "__main__":
    analyze_graph() 
