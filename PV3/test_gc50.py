#!/usr/bin/env python3
"""
Focused test for gc_50_9.txt instance
This will demonstrate our advanced hybrid algorithm's performance
"""

from graph_loader import load_graph
from heuristics import dsatur_coloring, welsh_powell_coloring, smallest_last_coloring
from genetic_algorithm import run_multistart_enhanced_algorithm, calculate_fitness

def test_gc50_instance():
    """Test specifically gc_50_9.txt with our advanced algorithm"""
    
    print("🚀 TESTING ADVANCED HYBRID ALGORITHM ON GC_50_9.TXT")
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
    
    # Now test our advanced algorithm
    print(f"\n🎯 TESTING ADVANCED HYBRID ALGORITHM")
    print("=" * 50)
    
    # Start from the best heuristic result and try to improve
    k_to_try = best_heuristic_k - 1
    final_result = best_heuristic_k
    
    while k_to_try > 0:
        print(f"\n🔍 Attempting {k_to_try} colors...")
        print("-" * 30)
        
        # Run multistart algorithm
        solution = run_multistart_enhanced_algorithm(
            graph, num_vertices, k_to_try, num_runs=3, verbose=True
        )
        
        if solution and calculate_fitness(solution, graph) == 0:
            final_result = k_to_try
            actual_colors = len(set(solution))
            print(f"✅ SUCCESS! Found valid coloring with {k_to_try} colors")
            print(f"   (Solution actually uses {actual_colors} distinct colors)")
            k_to_try -= 1
        else:
            print(f"❌ Failed to find solution with {k_to_try} colors")
            break
    
    # Summary
    print(f"\n🏆 FINAL RESULTS FOR GC_50_9.TXT:")
    print("=" * 50)
    print(f"Best heuristic (baseline): {best_heuristic_k} colors")
    print(f"Advanced hybrid result:    {final_result} colors")
    
    if final_result < best_heuristic_k:
        improvement = ((best_heuristic_k - final_result) / best_heuristic_k) * 100
        print(f"🎉 IMPROVEMENT: {improvement:.1f}% better!")
        print(f"   Reduced from {best_heuristic_k} to {final_result} colors")
    else:
        print("ℹ️  No improvement over heuristic baseline")
    
    return final_result, best_heuristic_k

if __name__ == "__main__":
    test_gc50_instance() 
