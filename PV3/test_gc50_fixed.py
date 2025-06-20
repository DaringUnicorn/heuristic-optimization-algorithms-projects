#!/usr/bin/env python3
"""
CORRECTED test for gc_50_9.txt instance
This will properly validate color constraints
"""

from graph_loader import load_graph
from heuristics import dsatur_coloring, welsh_powell_coloring, smallest_last_coloring
from genetic_algorithm import run_multistart_enhanced_algorithm, calculate_fitness

def is_valid_k_coloring(solution, adj_list, k):
    """
    Check if solution is a valid k-coloring:
    1. No conflicts (adjacent vertices have different colors)
    2. Uses at most k colors
    """
    if not solution:
        return False
    
    # Check conflicts
    if calculate_fitness(solution, adj_list) != 0:
        return False
    
    # Check color count constraint
    colors_used = len(set(solution))
    if colors_used > k:
        return False
    
    # Check if all colors are in valid range [1, k]
    if any(color < 1 or color > k for color in solution):
        return False
    
    return True

def test_gc50_corrected():
    """Corrected test for gc_50_9.txt with proper validation"""
    
    print("🚀 CORRECTED TEST: GC_50_9.TXT")
    print("=" * 60)
    
    # Load the graph
    num_vertices, num_edges, graph = load_graph('gc_50_9.txt')
    print(f"Graph loaded: {num_vertices} vertices, {num_edges} edges")
    
    # Test all heuristics first
    print("\n📊 BASELINE HEURISTIC RESULTS:")
    print("-" * 40)
    
    heuristics = [
        ("DSatur", dsatur_coloring),
        ("Welsh-Powell", welsh_powell_coloring), 
        ("Smallest-Last", smallest_last_coloring)
    ]
    
    best_heuristic_k = float('inf')
    for name, func in heuristics:
        k, _ = func(graph)
        print(f"{name:15}: {k:2d} colors")
        best_heuristic_k = min(best_heuristic_k, k)
    
    print(f"\nBest heuristic result: {best_heuristic_k} colors")
    
    # Now test our advanced algorithm with PROPER validation
    print(f"\n🎯 TESTING ADVANCED HYBRID ALGORITHM (WITH PROPER VALIDATION)")
    print("=" * 70)
    
    # Start from the best heuristic result and try to improve
    k_to_try = best_heuristic_k - 1
    final_result = best_heuristic_k
    
    while k_to_try > 0:
        print(f"\n🔍 Attempting {k_to_try} colors...")
        print("-" * 30)
        
        # Run multistart algorithm
        solution = run_multistart_enhanced_algorithm(
            graph, num_vertices, k_to_try, num_runs=2, verbose=False  # Less verbose for cleaner output
        )
        
        # PROPER VALIDATION
        if is_valid_k_coloring(solution, graph, k_to_try):
            actual_colors = len(set(solution))
            print(f"✅ SUCCESS! Found valid {k_to_try}-coloring")
            print(f"   Solution uses exactly {actual_colors} distinct colors")
            final_result = k_to_try
            k_to_try -= 1
        else:
            if solution:
                actual_colors = len(set(solution))
                conflicts = calculate_fitness(solution, graph)
                print(f"❌ FAILED {k_to_try}-coloring:")
                print(f"   - Solution uses {actual_colors} colors (exceeds limit)")
                print(f"   - Conflicts: {conflicts}")
            else:
                print(f"❌ FAILED {k_to_try}-coloring: No solution found")
            break
    
    # Summary
    print(f"\n🏆 CORRECTED RESULTS FOR GC_50_9.TXT:")
    print("=" * 50)
    print(f"Best heuristic (baseline): {best_heuristic_k} colors")
    print(f"Advanced hybrid result:    {final_result} colors")
    
    if final_result < best_heuristic_k:
        improvement = ((best_heuristic_k - final_result) / best_heuristic_k) * 100
        print(f"🎉 REAL IMPROVEMENT: {improvement:.1f}% better!")
        print(f"   Reduced from {best_heuristic_k} to {final_result} colors")
    else:
        print("ℹ️  No improvement over heuristic baseline")
        print("   (This is more realistic for dense graphs)")
    
    return final_result, best_heuristic_k

if __name__ == "__main__":
    test_gc50_corrected() 
