#!/usr/bin/env python3
"""
ADVANCED K-COLORING with Hybrid Techniques
Combines GA with backtracking and constraint propagation
"""

import random
from graph_loader import load_graph
from heuristics import dsatur_coloring

def can_color_vertex(vertex, color, assignment, adj_list):
    """Check if vertex can be colored with given color"""
    for neighbor in adj_list.get(vertex, []):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtrack_k_coloring(adj_list, num_vertices, k, partial_solution=None, timeout_generations=1000):
    """
    Backtracking algorithm for k-coloring with timeout
    """
    if partial_solution is None:
        partial_solution = {}
    
    vertices = list(range(num_vertices))
    # Sort vertices by degree (descending) - harder vertices first
    vertices.sort(key=lambda v: len(adj_list.get(v, [])), reverse=True)
    
    def backtrack_recursive(vertex_idx, generation_count):
        if generation_count > timeout_generations:
            return None  # Timeout
            
        if vertex_idx == len(vertices):
            return partial_solution.copy()  # Found solution
        
        vertex = vertices[vertex_idx]
        if vertex in partial_solution:
            return backtrack_recursive(vertex_idx + 1, generation_count + 1)
        
        # Try each color
        for color in range(1, k + 1):
            if can_color_vertex(vertex, color, partial_solution, adj_list):
                partial_solution[vertex] = color
                
                result = backtrack_recursive(vertex_idx + 1, generation_count + 1)
                if result is not None:
                    return result
                
                del partial_solution[vertex]  # Backtrack
        
        return None  # No solution found
    
    solution_dict = backtrack_recursive(0, 0)
    if solution_dict:
        # Convert to chromosome format
        return [solution_dict.get(i, 1) for i in range(num_vertices)]
    return None

def constraint_propagation_coloring(adj_list, num_vertices, k):
    """
    Constraint propagation approach
    """
    # For each vertex, maintain set of possible colors
    possible_colors = {v: set(range(1, k + 1)) for v in range(num_vertices)}
    assignment = {}
    
    # Sort vertices by degree (ascending) - easier vertices first for propagation
    vertices = sorted(range(num_vertices), key=lambda v: len(adj_list.get(v, [])))
    
    def propagate_constraints():
        """Remove impossible colors based on current assignments"""
        changed = True
        while changed:
            changed = False
            for vertex in range(num_vertices):
                if vertex in assignment:
                    continue
                    
                # Remove colors used by neighbors
                for neighbor in adj_list.get(vertex, []):
                    if neighbor in assignment:
                        neighbor_color = assignment[neighbor]
                        if neighbor_color in possible_colors[vertex]:
                            possible_colors[vertex].remove(neighbor_color)
                            changed = True
                
                # If only one color left, assign it
                if len(possible_colors[vertex]) == 1:
                    color = list(possible_colors[vertex])[0]
                    assignment[vertex] = color
                    changed = True
                elif len(possible_colors[vertex]) == 0:
                    return False  # No solution possible
        return True
    
    # Try to solve with constraint propagation
    for vertex in vertices:
        if vertex not in assignment:
            if not propagate_constraints():
                return None
            
            if vertex not in assignment:
                # Choose color with minimum remaining values heuristic
                if possible_colors[vertex]:
                    color = min(possible_colors[vertex])
                    assignment[vertex] = color
                else:
                    return None
    
    if len(assignment) == num_vertices:
        return [assignment.get(i, 1) for i in range(num_vertices)]
    return None

def hybrid_k_coloring_attack(adj_list, num_vertices, k, verbose=True):
    """
    Multi-pronged attack on k-coloring problem
    """
    if verbose:
        print(f"\n🚀 HYBRID K-COLORING ATTACK for k={k}")
        print("=" * 60)
    
    # Method 1: Constraint Propagation
    if verbose:
        print(f"🔧 Method 1: Constraint Propagation...")
    
    solution = constraint_propagation_coloring(adj_list, num_vertices, k)
    if solution:
        conflicts = sum(1 for u in adj_list for v in adj_list[u] 
                       if u < v and solution[u] == solution[v])
        colors_used = len(set(solution))
        if conflicts == 0 and colors_used <= k:
            if verbose:
                print(f"✅ SUCCESS with Constraint Propagation!")
                print(f"   Colors used: {colors_used}")
            return solution
    
    if verbose:
        print(f"❌ Constraint Propagation failed")
    
    # Method 2: Backtracking with smart ordering
    if verbose:
        print(f"🔧 Method 2: Backtracking...")
    
    solution = backtrack_k_coloring(adj_list, num_vertices, k, timeout_generations=5000)
    if solution:
        conflicts = sum(1 for u in adj_list for v in adj_list[u] 
                       if u < v and solution[u] == solution[v])
        colors_used = len(set(solution))
        if conflicts == 0 and colors_used <= k:
            if verbose:
                print(f"✅ SUCCESS with Backtracking!")
                print(f"   Colors used: {colors_used}")
            return solution
    
    if verbose:
        print(f"❌ Backtracking failed")
    
    # Method 3: Multiple random restarts with greedy
    if verbose:
        print(f"🔧 Method 3: Random Restart Greedy...")
    
    for attempt in range(100):
        vertices = list(range(num_vertices))
        random.shuffle(vertices)  # Random ordering
        
        assignment = {}
        failed = False
        
        for vertex in vertices:
            available_colors = set(range(1, k + 1))
            for neighbor in adj_list.get(vertex, []):
                if neighbor in assignment:
                    available_colors.discard(assignment[neighbor])
            
            if available_colors:
                assignment[vertex] = random.choice(list(available_colors))
            else:
                failed = True
                break
        
        if not failed and len(assignment) == num_vertices:
            solution = [assignment.get(i, 1) for i in range(num_vertices)]
            conflicts = sum(1 for u in adj_list for v in adj_list[u] 
                           if u < v and solution[u] == solution[v])
            colors_used = len(set(solution))
            
            if conflicts == 0 and colors_used <= k:
                if verbose:
                    print(f"✅ SUCCESS with Random Restart (attempt {attempt + 1})!")
                    print(f"   Colors used: {colors_used}")
                return solution
    
    if verbose:
        print(f"❌ Random Restart failed after 100 attempts")
    
    return None

def comprehensive_k_coloring_test():
    """
    Comprehensive test of advanced k-coloring techniques
    """
    print("🚀 COMPREHENSIVE K-COLORING TEST")
    print("=" * 60)
    
    # Load graph
    num_vertices, num_edges, graph = load_graph('gc_50_9.txt')
    print(f"Graph: {num_vertices} vertices, {num_edges} edges")
    
    # Get baseline
    k_dsatur, _ = dsatur_coloring(graph)
    print(f"DSatur baseline: {k_dsatur} colors")
    
    # Try advanced techniques
    best_result = k_dsatur
    
    for k_target in range(k_dsatur - 1, max(k_dsatur - 3, 1), -1):
        print(f"\n{'='*50}")
        print(f"🎯 ATTEMPTING k={k_target}")
        print(f"{'='*50}")
        
        solution = hybrid_k_coloring_attack(graph, num_vertices, k_target, verbose=True)
        
        if solution:
            actual_colors = len(set(solution))
            conflicts = sum(1 for u in graph for v in graph[u] 
                           if u < v and solution[u] == solution[v])
            
            print(f"\n🎉 BREAKTHROUGH! Found {k_target}-coloring!")
            print(f"   ✅ Uses {actual_colors} distinct colors")
            print(f"   ✅ Conflicts: {conflicts}")
            print(f"   ✅ All colors in range [1, {k_target}]: {all(1 <= c <= k_target for c in solution)}")
            
            best_result = k_target
        else:
            print(f"\n❌ Could not find {k_target}-coloring")
            break
    
    # Final summary
    print(f"\n🏆 FINAL COMPREHENSIVE RESULTS:")
    print("=" * 50)
    print(f"DSatur baseline:     {k_dsatur} colors")
    print(f"Advanced techniques: {best_result} colors")
    
    if best_result < k_dsatur:
        improvement = ((k_dsatur - best_result) / k_dsatur) * 100
        print(f"🎉 IMPROVEMENT: {improvement:.1f}% better!")
    else:
        print("ℹ️  No improvement found")
        print("   This suggests DSatur found near-optimal solution")
    
    return best_result

if __name__ == "__main__":
    comprehensive_k_coloring_test() 
