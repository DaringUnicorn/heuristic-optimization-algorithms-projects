#!/usr/bin/env python3
"""
FINAL TEST: Check the limits of k-coloring
"""

from graph_loader import load_graph
from heuristics import dsatur_coloring
import time

def test_k_limits():
    """Test different k values to find the limit"""
    
    print("🎯 FINAL K-COLORING LIMIT TEST")
    print("=" * 50)
    
    # Load graph
    num_vertices, num_edges, graph = load_graph('gc_50_9.txt')
    print(f"Graph: {num_vertices} vertices, {num_edges} edges")
    
    # Get baseline
    dsatur_k, _ = dsatur_coloring(graph)
    print(f"DSatur baseline: {dsatur_k} colors")
    
    def backtrack_k_coloring(k, timeout_calls=50000):
        """Simple backtracking with call limit"""
        assignment = {}
        vertices = list(range(num_vertices))
        vertices.sort(key=lambda v: len(graph.get(v, [])), reverse=True)
        
        call_count = 0
        
        def can_color(vertex, color):
            for neighbor in graph.get(vertex, []):
                if neighbor in assignment and assignment[neighbor] == color:
                    return False
            return True
        
        def backtrack(vertex_idx):
            nonlocal call_count
            call_count += 1
            
            if call_count > timeout_calls:
                return False
                
            if vertex_idx >= len(vertices):
                return True
            
            vertex = vertices[vertex_idx]
            
            for color in range(1, k + 1):
                if can_color(vertex, color):
                    assignment[vertex] = color
                    
                    if backtrack(vertex_idx + 1):
                        return True
                    
                    del assignment[vertex]
            
            return False
        
        start_time = time.time()
        success = backtrack(0)
        end_time = time.time()
        
        return success, call_count, end_time - start_time, assignment
    
    # Test different k values
    print(f"\n🧪 TESTING DIFFERENT K VALUES:")
    print(f"{'k':>3} | {'Success':>8} | {'Calls':>8} | {'Time':>8} | {'Status'}")
    print("-" * 50)
    
    results = {}
    
    for k in range(23, 16, -1):  # From 23 down to 17
        success, calls, time_taken, assignment = backtrack_k_coloring(k, timeout_calls=100000)
        
        status = "✅ FOUND" if success else "❌ FAILED"
        if calls >= 100000:
            status = "⏰ TIMEOUT"
        
        results[k] = success
        
        print(f"{k:>3} | {str(success):>8} | {calls:>8} | {time_taken:>6.3f}s | {status}")
        
        if not success and calls < 100000:
            print(f"    └─ PROVEN IMPOSSIBLE with {calls} calls")
            break
    
    # Find the chromatic number
    print(f"\n🎨 CHROMATIC NUMBER ANALYSIS:")
    
    successful_k = [k for k, success in results.items() if success]
    failed_k = [k for k, success in results.items() if not success]
    
    if successful_k:
        min_successful = min(successful_k)
        print(f"   Minimum successful k: {min_successful}")
    
    if failed_k:
        max_failed = max(failed_k)
        print(f"   Maximum failed k: {max_failed}")
        
        if successful_k:
            chromatic_lower = max_failed + 1
            chromatic_upper = min_successful
            
            if chromatic_lower == chromatic_upper:
                print(f"   🎯 CHROMATIC NUMBER = {chromatic_lower}")
            else:
                print(f"   📊 CHROMATIC NUMBER ∈ [{chromatic_lower}, {chromatic_upper}]")
    
    print(f"\n📈 COMPARISON:")
    print(f"   DSatur: {dsatur_k} colors")
    if successful_k:
        improvement = dsatur_k - min_successful
        percentage = improvement / dsatur_k * 100
        print(f"   Backtrack: {min_successful} colors")
        print(f"   Improvement: {improvement} colors ({percentage:.1f}%)")
        
        if improvement > 0:
            print(f"   🎉 GENUINE IMPROVEMENT ACHIEVED!")
        else:
            print(f"   😐 No improvement over DSatur")

if __name__ == "__main__":
    test_k_limits() 
