import glob
import csv

from graph_loader import load_graph
from heuristics import dsatur_coloring, welsh_powell_coloring, smallest_last_coloring, get_diverse_initial_solutions
from genetic_algorithm import run_multistart_enhanced_algorithm, calculate_fitness

def find_best_coloring(graph, num_vertices, start_k, algorithm_func, verbose_name):
    """Helper function to iteratively find the best k for a given algorithm."""
    final_k = start_k
    k_to_try = start_k - 1
    
    while k_to_try > 0:  # Prevent trying 0 colors
        print(f"\n[{verbose_name}] Attempting to find a solution with {k_to_try} colors...")
        # verbose=True to show step-by-step progress
        solution = algorithm_func(graph, num_vertices, k_to_try, verbose=True) 
        
        if solution and calculate_fitness(solution, graph) == 0:
            final_k = k_to_try
            print(f"[{verbose_name}] Success! Found a valid coloring with {final_k} colors.")
            k_to_try -= 1
        else:
            print(f"[{verbose_name}] Failed to find a better solution. Best is {final_k} colors.")
            break
    return final_k

def test_all_heuristics(graph):
    """Test all available heuristics and return the best result as starting point."""
    print("\n=== Testing All Heuristic Algorithms ===")
    
    heuristics = [
        ("DSatur", dsatur_coloring),
        ("Welsh-Powell", welsh_powell_coloring), 
        ("Smallest-Last", smallest_last_coloring)
    ]
    
    best_k = float('inf')
    best_name = ""
    
    for name, func in heuristics:
        k, _ = func(graph)
        print(f"{name}: {k} colors")
        if k < best_k:
            best_k = k
            best_name = name
    
    print(f"\nBest heuristic: {best_name} with {best_k} colors")
    return best_k

def main():
    """
    Main function to run the graph coloring project.
    Tests all heuristics, then runs the advanced hybrid algorithm.
    """
    graph_files = sorted(glob.glob('gc_*.txt'))
    if not graph_files:
        print("No graph files found.")
        return

    # Test all instances to see comprehensive improvements
    graph_files = ['gc_50_9.txt', 'gc_70_9.txt', 'gc_100_9.txt', 'gc_250_9.txt']
    print(f"Running comprehensive analysis on all main files: {graph_files}")

    results = []
    for file_name in graph_files:
        print(f"\n{'='*60}")
        print(f"PROCESSING {file_name}")
        print(f"{'='*60}")
        
        num_vertices, num_edges, graph = load_graph(file_name)

        if not graph:
            continue

        print(f"Graph loaded: {num_vertices} vertices, {num_edges} edges.")
        
        # Test all heuristics first
        best_heuristic_k = test_all_heuristics(graph)
        
        # Run the advanced hybrid algorithm with multistart
        print(f"\n=== Running Advanced Hybrid Algorithm (MULTISTART) ===")
        final_k = find_best_coloring(graph, num_vertices, best_heuristic_k, run_multistart_enhanced_algorithm, "MULTISTART Hybrid MA")

        results.append({
            'File': file_name,
            'Vertices': num_vertices,
            'Edges': num_edges,
            'Best Heuristic (k)': best_heuristic_k,
                         'MULTISTART Hybrid MA (k)': final_k
        })

    if results:
        print(f"\n{'='*80}")
        print("FINAL COMPREHENSIVE RESULTS")
        print(f"{'='*80}")
        headers = results[0].keys()
        col_widths = {h: max(len(str(r[h])) for r in results) for h in headers}
        for h in headers:
            col_widths[h] = max(col_widths[h], len(h))
        
        header_line = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
        print(header_line)
        print("-" * len(header_line))

        for res in results:
            row_line = " | ".join(f"{str(res[h]):<{col_widths[h]}}" for h in headers)
            print(row_line)

        try:
            with open('ultimate_results.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(results)
            print("\nResults have been saved to ultimate_results.csv")
        except IOError as e:
            print(f"\nCould not write to ultimate_results.csv: {e}")

if __name__ == '__main__':
    main()
