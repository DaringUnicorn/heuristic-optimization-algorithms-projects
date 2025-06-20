import os
import json
import csv
from datetime import datetime
from utils import parse_dimacs_graph
from initializers import dsatur_initializer, greedy_initializer
from base_genetic_algorithm import GeneticAlgorithm

def test_heuristic_on_graph(graph, heuristic_name, heuristic_func, max_colors=15):
    """
    Test a heuristic algorithm on a graph with different color counts.
    """
    print(f"\nTesting {heuristic_name} on graph with {graph.num_vertices} vertices and {graph.num_edges} edges")
    print("-" * 60)
    
    best_result = None
    best_colors = None
    
    for num_colors in range(1, max_colors + 1):
        try:
            # Generate coloring using the heuristic
            coloring = heuristic_func(graph, num_colors)
            
            # Calculate conflicts
            conflicts = 0
            for vertex, neighbors in graph.adj.items():
                for neighbor in neighbors:
                    if vertex < neighbor and coloring[vertex] == coloring[neighbor]:
                        conflicts += 1
            
            # Calculate unique colors used
            unique_colors = len(set(coloring))
            
            print(f"Colors: {num_colors:2d} | Conflicts: {conflicts:3d} | Unique Colors Used: {unique_colors:2d}")
            
            # Check if this is a valid solution (no conflicts)
            if conflicts == 0:
                if best_result is None or unique_colors < best_result:
                    best_result = unique_colors
                    best_colors = num_colors
                    print(f"  ✅ VALID SOLUTION FOUND! Using {unique_colors} colors")
                    break  # Found optimal solution, no need to test more colors
                    
        except Exception as e:
            print(f"Colors: {num_colors:2d} | Error: {e}")
    
    if best_result is not None:
        print(f"\n🎯 OPTIMAL SOLUTION: {best_result} colors needed")
    else:
        print(f"\n❌ No valid solution found with up to {max_colors} colors")
    
    return best_result, best_colors

def dsatur_classic(graph):
    """
    Classic DSATUR algorithm without color limits.
    Returns the coloring and the number of colors used.
    """
    n = graph.num_vertices
    colors = [-1] * n
    saturation = [0] * n
    degrees = [len(graph.adj[v]) for v in range(n)]
    uncolored = set(range(n))
    max_color_used = -1

    while uncolored:
        # Select vertex with highest saturation, break ties by degree
        max_sat = max(saturation[v] for v in uncolored)
        candidates = [v for v in uncolored if saturation[v] == max_sat]
        if len(candidates) > 1:
            v = max(candidates, key=lambda x: degrees[x])
        else:
            v = candidates[0]
        
        # Find the smallest available color
        neighbor_colors = set(colors[u] for u in graph.adj[v] if colors[u] != -1)
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[v] = color
        max_color_used = max(max_color_used, color)
        
        # Update saturation of neighbors
        for u in graph.adj[v]:
            if colors[u] == -1:
                neighbor_colors_u = set(colors[w] for w in graph.adj[u] if colors[w] != -1)
                saturation[u] = len(neighbor_colors_u)
        uncolored.remove(v)
    
    return colors, max_color_used + 1

def greedy_classic(graph):
    """
    Classic Greedy algorithm without color limits.
    Returns the coloring and the number of colors used.
    """
    n = graph.num_vertices
    colors = [-1] * n
    max_color_used = -1
    
    for v in range(n):
        # Find the smallest available color for this vertex
        neighbor_colors = set(colors[u] for u in graph.adj[v] if colors[u] != -1)
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[v] = color
        max_color_used = max(max_color_used, color)
    
    return colors, max_color_used + 1

def calculate_conflicts(graph, coloring):
    """
    Calculate the number of conflicts in a coloring.
    """
    conflicts = 0
    for vertex, neighbors in graph.adj.items():
        for neighbor in neighbors:
            if vertex < neighbor and coloring[vertex] == coloring[neighbor]:
                conflicts += 1
    return conflicts

def test_classic_heuristics(graph, graph_name):
    """
    Test classic DSATUR and Greedy algorithms on a graph.
    """
    print(f"\n{'='*80}")
    print(f"TESTING CLASSIC HEURISTICS ON: {graph_name}")
    print(f"{'='*80}")
    print(f"Graph: {graph.num_vertices} vertices, {graph.num_edges} edges")
    print("-" * 60)
    
    # Test DSATUR
    print("\n🔍 Testing DSATUR (Classic):")
    dsatur_coloring, dsatur_colors = dsatur_classic(graph)
    dsatur_conflicts = calculate_conflicts(graph, dsatur_coloring)
    print(f"  Colors used: {dsatur_colors}")
    print(f"  Conflicts: {dsatur_conflicts}")
    print(f"  Valid solution: {'✅ YES' if dsatur_conflicts == 0 else '❌ NO'}")
    
    # Test Greedy
    print("\n🔍 Testing Greedy (Classic):")
    greedy_coloring, greedy_colors = greedy_classic(graph)
    greedy_conflicts = calculate_conflicts(graph, greedy_coloring)
    print(f"  Colors used: {greedy_colors}")
    print(f"  Conflicts: {greedy_conflicts}")
    print(f"  Valid solution: {'✅ YES' if greedy_conflicts == 0 else '❌ NO'}")
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"  DSATUR: {dsatur_colors} colors, {dsatur_conflicts} conflicts")
    print(f"  Greedy: {greedy_colors} colors, {greedy_conflicts} conflicts")
    
    if dsatur_conflicts == 0 and greedy_conflicts == 0:
        best = min(dsatur_colors, greedy_colors)
        print(f"  🎯 Best valid solution: {best} colors")
    elif dsatur_conflicts == 0:
        print(f"  🎯 Best valid solution: DSATUR with {dsatur_colors} colors")
    elif greedy_conflicts == 0:
        print(f"  🎯 Best valid solution: Greedy with {greedy_colors} colors")
    else:
        print(f"  ⚠️  No valid solution found by either algorithm")
    
    return {
        'dsatur_colors': dsatur_colors,
        'dsatur_conflicts': dsatur_conflicts,
        'greedy_colors': greedy_colors,
        'greedy_conflicts': greedy_conflicts
    }

def save_results_to_file(results, filename="heuristic_test_results.json"):
    """
    Save test results to a JSON file.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "..", "results")
    
    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)
    
    file_path = os.path.join(results_dir, filename)
    
    # Add timestamp to results
    results['timestamp'] = datetime.now().isoformat()
    
    with open(file_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {file_path}")
    return file_path

def run_ga_test(graph, num_colors, population_size=100, generations=100, initializer="mixed"):
    """
    Run Genetic Algorithm test with specified parameters.
    """
    print(f"\n🧬 Testing Genetic Algorithm:")
    print(f"  Colors: {num_colors}")
    print(f"  Population: {population_size}")
    print(f"  Generations: {generations}")
    print(f"  Initializer: {initializer}")
    print("-" * 50)
    
    ga = GeneticAlgorithm(
        graph=graph,
        population_size=population_size,
        num_colors=num_colors,
        initializer=initializer
    )
    
    best_chromosome, best_fitness, best_conflicts, best_colors = ga.run(generations=generations)
    
    return {
        'best_fitness': best_fitness,
        'best_conflicts': best_conflicts,
        'best_colors_used': best_colors,
        'valid_solution': best_conflicts == 0
    }

def save_consolidated_results_to_csv(all_results, filename="consolidated_results.csv"):
    """
    Save consolidated results to a clean CSV file with one row per algorithm per graph.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    file_path = os.path.join(results_dir, filename)
    
    # Create consolidated results
    consolidated = []
    
    for graph_file, results in all_results.items():
        # Add classic heuristics
        if 'classic' in results:
            classic = results['classic']
            consolidated.append({
                'graph_file': graph_file,
                'algorithm': 'DSATUR',
                'initializer': 'N/A',
                'num_colors': 'N/A',
                'colors_used': classic['dsatur_colors'],
                'conflicts': classic['dsatur_conflicts'],
                'valid_solution': classic['dsatur_conflicts'] == 0,
                'best_fitness': 'N/A',
                'vertices': classic.get('vertices', ''),
                'edges': classic.get('edges', '')
            })
            
            consolidated.append({
                'graph_file': graph_file,
                'algorithm': 'Greedy',
                'initializer': 'N/A',
                'num_colors': 'N/A',
                'colors_used': classic['greedy_colors'],
                'conflicts': classic['greedy_conflicts'],
                'valid_solution': classic['greedy_conflicts'] == 0,
                'best_fitness': 'N/A',
                'vertices': classic.get('vertices', ''),
                'edges': classic.get('edges', '')
            })
        
        # Add GA results (best result per initializer)
        if 'ga' in results:
            ga_results = results['ga']
            best_per_initializer = {}
            
            for key, result in ga_results.items():
                if '_' in key:
                    num_colors, initializer = key.split('_', 1)
                    if initializer not in best_per_initializer or result['best_conflicts'] < best_per_initializer[initializer]['best_conflicts']:
                        best_per_initializer[initializer] = result
            
            for initializer, result in best_per_initializer.items():
                consolidated.append({
                    'graph_file': graph_file,
                    'algorithm': 'Genetic Algorithm',
                    'initializer': initializer,
                    'num_colors': result.get('num_colors', ''),
                    'colors_used': result.get('best_colors_used', ''),
                    'conflicts': result.get('best_conflicts', ''),
                    'valid_solution': result.get('valid_solution', ''),
                    'best_fitness': result.get('best_fitness', ''),
                    'vertices': result.get('vertices', ''),
                    'edges': result.get('edges', '')
                })
    
    # Write to CSV
    fieldnames = [
        'graph_file', 'algorithm', 'initializer', 'num_colors', 'colors_used', 
        'conflicts', 'valid_solution', 'best_fitness', 'vertices', 'edges'
    ]
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in consolidated:
            writer.writerow(row)
    
    print(f"\n💾 Consolidated results saved to: {file_path}")
    return file_path

def main():
    """
    Test classic heuristics and save results, then run GA tests.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    file_name = "gc_50_9.txt"
    file_path = os.path.join(data_dir, file_name)
    
    print("=" * 80)
    print("COMPREHENSIVE GRAPH COLORING TESTING")
    print("=" * 80)
    
    all_results = {}
    
    try:
        # Load graph
        graph = parse_dimacs_graph(file_path)
        
        # Test classic heuristics
        classic_results = test_classic_heuristics(graph, file_name)
        classic_results['vertices'] = graph.num_vertices
        classic_results['edges'] = graph.num_edges
        
        # Save classic results
        save_results_to_file(classic_results, "classic_heuristics_results.json")
        
        # Determine color range for GA testing
        max_colors = max(classic_results['dsatur_colors'], classic_results['greedy_colors'])
        min_colors = min(classic_results['dsatur_colors'], classic_results['greedy_colors'])
        
        print(f"\n{'='*80}")
        print("GENETIC ALGORITHM TESTING")
        print(f"{'='*80}")
        
        # Test GA with different parameters
        ga_results = {}
        
        # Test with different color counts
        for num_colors in range(min_colors, max_colors + 3):
            print(f"\n--- Testing with {num_colors} colors ---")
            
            # Test with different initializers
            for initializer in ["random", "dsatur", "greedy", "mixed"]:
                result = run_ga_test(graph, num_colors, 100, 100, initializer)
                result['num_colors'] = num_colors
                result['vertices'] = graph.num_vertices
                result['edges'] = graph.num_edges
                ga_results[f"{num_colors}colors_{initializer}"] = result
                
                if result['valid_solution']:
                    print(f"  ✅ {initializer}: Valid solution found!")
                    break
            else:
                print(f"  ❌ No valid solution found with {num_colors} colors")
        
        # Save GA results
        save_results_to_file(ga_results, "genetic_algorithm_results.json")
        
        # Store results for consolidation
        all_results[file_name] = {
            'classic': classic_results,
            'ga': ga_results
        }
        
        # Save consolidated results
        save_consolidated_results_to_csv(all_results, "consolidated_results.csv")
        
        # Print final summary
        print(f"\n{'='*80}")
        print("FINAL SUMMARY")
        print(f"{'='*80}")
        print(f"Classic DSATUR: {classic_results['dsatur_colors']} colors, {classic_results['dsatur_conflicts']} conflicts")
        print(f"Classic Greedy: {classic_results['greedy_colors']} colors, {classic_results['greedy_conflicts']} conflicts")
        
        # Check if GA found any valid solutions
        valid_ga_solutions = [k for k, v in ga_results.items() if v['valid_solution']]
        if valid_ga_solutions:
            print(f"✅ GA found valid solutions: {valid_ga_solutions}")
        else:
            print(f"❌ GA did not find any valid solutions")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 
