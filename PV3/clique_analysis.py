#!/usr/bin/env python3
"""
CLIQUE ANALYSIS: Careful analysis of cliques in the graph
"""

from graph_loader import load_graph

def find_max_clique():
    """Find the maximum clique more carefully"""
    
    print("🔍 CAREFUL CLIQUE ANALYSIS")
    print("=" * 40)
    
    # Load graph
    num_vertices, num_edges, graph = load_graph('gc_50_9.txt')
    
    def is_clique(vertices):
        """Check if a set of vertices forms a clique"""
        vertices = list(vertices)
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                v1, v2 = vertices[i], vertices[j]
                if v2 not in graph.get(v1, []):
                    return False
        return True
    
    def find_clique_from_vertex(start_vertex):
        """Find largest clique containing start_vertex"""
        clique = {start_vertex}
        candidates = set(graph.get(start_vertex, []))
        
        while candidates:
            # Find vertex in candidates that is connected to all in clique
            best_vertex = None
            best_connections = -1
            
            for candidate in candidates:
                connections = sum(1 for v in clique if candidate in graph.get(v, []))
                if connections == len(clique) and connections > best_connections:
                    best_vertex = candidate
                    best_connections = connections
            
            if best_vertex is not None:
                clique.add(best_vertex)
                # Update candidates - only those connected to all in clique
                new_candidates = set()
                for candidate in candidates:
                    if candidate != best_vertex:
                        connected_to_all = all(candidate in graph.get(v, []) for v in clique)
                        if connected_to_all:
                            new_candidates.add(candidate)
                candidates = new_candidates
            else:
                break
        
        return clique
    
    print(f"🔍 Finding maximum clique...")
    
    max_clique = set()
    max_size = 0
    
    # Try from a few high-degree vertices
    degrees = [(len(graph.get(v, [])), v) for v in range(num_vertices)]
    degrees.sort(reverse=True)
    
    for degree, vertex in degrees[:10]:  # Top 10 highest degree
        clique = find_clique_from_vertex(vertex)
        if len(clique) > max_size:
            max_clique = clique
            max_size = len(clique)
        print(f"   Vertex {vertex} (degree {degree}): clique size {len(clique)}")
    
    print(f"\n📊 RESULTS:")
    print(f"   Maximum clique size found: {max_size}")
    print(f"   Maximum clique: {sorted(max_clique)}")
    
    # Verify the clique
    if is_clique(max_clique):
        print(f"   ✅ Verified: This is indeed a clique")
    else:
        print(f"   ❌ ERROR: This is not a valid clique!")
    
    # Lower bound for chromatic number
    print(f"\n🎨 COLORING IMPLICATIONS:")
    print(f"   Lower bound (clique): {max_size} colors needed")
    print(f"   DSatur found: 23 colors")
    print(f"   Backtrack found: 22 colors")
    
    if max_size > 22:
        print(f"   🚨 IMPOSSIBLE! Need at least {max_size} colors!")
        print(f"      Either clique analysis is wrong OR")
        print(f"      coloring algorithms are wrong")
    elif max_size <= 22:
        print(f"   ✅ Possible: {max_size} ≤ 22, so 22-coloring could exist")
    
    # Detailed check of the clique
    if max_clique:
        print(f"\n🔬 DETAILED CLIQUE VERIFICATION:")
        clique_list = list(max_clique)
        missing_edges = []
        
        for i in range(len(clique_list)):
            for j in range(i + 1, len(clique_list)):
                v1, v2 = clique_list[i], clique_list[j]
                if v2 not in graph.get(v1, []):
                    missing_edges.append((v1, v2))
        
        if missing_edges:
            print(f"   ❌ Missing edges in 'clique': {missing_edges[:5]}...")
            print(f"      Total missing: {len(missing_edges)}")
        else:
            print(f"   ✅ All edges present - valid clique")
    
    return max_size, max_clique

if __name__ == "__main__":
    find_max_clique() 
