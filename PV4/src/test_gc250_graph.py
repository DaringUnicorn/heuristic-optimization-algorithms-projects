import os
import time
from utils import parse_dimacs_graph
from hybrid_genetic_algorithms import GATabuSearch, GAAdaptiveRepair, MemeticGA, GAGreedyCustomCrossover, GreedyInitializer
from base_genetic_algorithm import GeneticAlgorithm

def test_gc250():
    """
    Test all four hybrid algorithms on gc_250_9.txt
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    file_path = os.path.join(data_dir, "gc_250_9.txt")
    
    print("=" * 80)
    print("Testing ALL FOUR Hybrid Algorithms on gc_250_9.txt")
    print("=" * 80)

    try:
        # Load the graph
        print(f"Loading graph from {file_path}...")
        graph = parse_dimacs_graph(file_path)
        print(f"✅ Graph loaded successfully!")
        print(f"   Vertices: {len(graph.adj)}")
        print(f"   Edges: {sum(len(neighbors) for neighbors in graph.adj.values()) // 2}")
        
        # Use Greedy algorithm to estimate the actual number of colors needed
        print(f"\n--- Estimating required colors using Greedy algorithm ---")
        greedy_initializer = GreedyInitializer(graph)
        greedy_solution, greedy_colors = greedy_initializer.greedy_coloring()
        print(f"   Greedy algorithm uses {greedy_colors} colors")
        
        # Use the greedy result as our color estimate (with some buffer)
        num_colors = greedy_colors + 5  # Add buffer for optimization
        print(f"   Using {num_colors} colors for all algorithms (greedy + buffer)")
        
        # Test parameters - reduced for larger graph
        population_size = 20  # Smaller population for larger graphs
        generations = 20      # Fewer generations for faster testing
        
        print(f"\nTest Parameters:")
        print(f"   Population Size: {population_size}")
        print(f"   Generations: {generations}")
        print(f"   Colors: {num_colors}")

        # --- Test GA + DSATUR + Tabu Search ---
        print("\n\n--- METHOD 1: GA + DSATUR + Tabu Search ---")
        start_time = time.time()
        ga_ts = GATabuSearch(
            graph=graph,
            population_size=population_size,
            num_colors=num_colors,
            tabu_iterations=300,  # Reduced for larger graphs
            tabu_tenure=8
        )

        best_chromosome, best_fitness, best_conflicts, best_colors = ga_ts.run(generations=generations)
        ts_time = time.time() - start_time

        print(f"\n--- Final Result for GA+TS ---")
        print(f"  Best solution has {best_conflicts} conflicts.")
        print(f"  Colors used: {best_colors}")
        print(f"  Runtime: {ts_time:.2f} seconds")
        if best_conflicts == 0:
            print("  ✅ VALID SOLUTION FOUND!")
        else:
            print("  ❌ No valid solution found.")

        # --- Test GA + Constraint Repair + Adaptive Parameters ---
        print("\n\n--- METHOD 2: GA + Constraint Repair + Adaptive Parameters ---")
        start_time = time.time()
        ga_adaptive = GAAdaptiveRepair(
            graph=graph,
            population_size=population_size,
            num_colors=num_colors,
            base_mutation_rate=0.15,
            diversity_threshold=0.25
        )

        best_chromosome2, best_fitness2, best_conflicts2, best_colors2 = ga_adaptive.run(generations=generations)
        adaptive_time = time.time() - start_time

        print(f"\n--- Final Result for GA+Adaptive+Repair ---")
        print(f"  Best solution has {best_conflicts2} conflicts.")
        print(f"  Colors used: {best_colors2}")
        print(f"  Runtime: {adaptive_time:.2f} seconds")
        if best_conflicts2 == 0:
            print("  ✅ VALID SOLUTION FOUND!")
        else:
            print("  ❌ No valid solution found.")

        # --- Test Memetic GA ---
        print("\n\n--- METHOD 3: Memetic GA ---")
        start_time = time.time()
        memetic_ga = MemeticGA(
            graph=graph,
            population_size=population_size,
            num_colors=num_colors,
            local_search_type="tabu",
            local_search_iterations=10  # Reduced for larger graphs
        )

        best_chromosome3, best_fitness3, best_conflicts3, best_colors3 = memetic_ga.run(generations=generations)
        memetic_time = time.time() - start_time

        print(f"\n--- Final Result for Memetic GA ---")
        print(f"  Best solution has {best_conflicts3} conflicts.")
        print(f"  Colors used: {best_colors3}")
        print(f"  Runtime: {memetic_time:.2f} seconds")
        if best_conflicts3 == 0:
            print("  ✅ VALID SOLUTION FOUND!")
        else:
            print("  ❌ No valid solution found.")

        # --- Test GA + Greedy + Custom Crossover ---
        print("\n\n--- METHOD 4: GA + Greedy + Custom Crossover ---")
        start_time = time.time()
        ga_greedy_custom = GAGreedyCustomCrossover(
            graph=graph,
            population_size=population_size,
            num_colors=num_colors,
            local_search_iterations=8  # Reduced for larger graphs
        )

        best_chromosome4, best_fitness4, best_conflicts4, best_colors4 = ga_greedy_custom.run(generations=generations)
        greedy_time = time.time() - start_time

        print(f"\n--- Final Result for GA+Greedy+Custom ---")
        print(f"  Best solution has {best_conflicts4} conflicts.")
        print(f"  Colors used: {best_colors4}")
        print(f"  Runtime: {greedy_time:.2f} seconds")
        if best_conflicts4 == 0:
            print("  ✅ VALID SOLUTION FOUND!")
        else:
            print("  ❌ No valid solution found.")

        # --- Comparison ---
        print("\n\n--- COMPARISON OF ALL FOUR METHODS ---")
        print(f"Graph: gc_250_9.txt")
        print(f"Vertices: {len(graph.adj)}, Edges: {sum(len(neighbors) for neighbors in graph.adj.values()) // 2}")
        print(f"Greedy estimate: {greedy_colors} colors")
        print(f"{'='*60}")
        print(f"{'Algorithm':<35} {'Conflicts':<10} {'Colors':<8} {'Runtime':<10}")
        print(f"{'='*60}")
        print(f"{'GA + DSATUR + Tabu Search':<35} {best_conflicts:<10} {best_colors:<8} {ts_time:<10.2f}s")
        print(f"{'GA + Adaptive + Repair':<35} {best_conflicts2:<10} {best_colors2:<8} {adaptive_time:<10.2f}s")
        print(f"{'Memetic GA':<35} {best_conflicts3:<10} {best_colors3:<8} {memetic_time:<10.2f}s")
        print(f"{'GA + Greedy + Custom Crossover':<35} {best_conflicts4:<10} {best_colors4:<8} {greedy_time:<10.2f}s")
        print(f"{'='*60}")
        
        # Find the best algorithm
        valid_solutions = []
        if best_conflicts == 0:
            valid_solutions.append(("GA + DSATUR + Tabu Search", best_colors, ts_time))
        if best_conflicts2 == 0:
            valid_solutions.append(("GA + Adaptive + Repair", best_colors2, adaptive_time))
        if best_conflicts3 == 0:
            valid_solutions.append(("Memetic GA", best_colors3, memetic_time))
        if best_conflicts4 == 0:
            valid_solutions.append(("GA + Greedy + Custom Crossover", best_colors4, greedy_time))
        
        if len(valid_solutions) > 0:
            print(f"\n🎉 {len(valid_solutions)} methods found valid solutions!")
            # Sort by colors used, then by runtime
            valid_solutions.sort(key=lambda x: (x[1], x[2]))
            best_algorithm = valid_solutions[0]
            print(f"🏆 Best algorithm: {best_algorithm[0]}")
            print(f"   Colors: {best_algorithm[1]}, Runtime: {best_algorithm[2]:.2f}s")
        else:
            print("\n❌ No method found a valid solution")
            # Find the one with least conflicts
            all_results = [
                ("GA + DSATUR + Tabu Search", best_conflicts, best_colors, ts_time),
                ("GA + Adaptive + Repair", best_conflicts2, best_colors2, adaptive_time),
                ("Memetic GA", best_conflicts3, best_colors3, memetic_time),
                ("GA + Greedy + Custom Crossover", best_conflicts4, best_colors4, greedy_time)
            ]
            best_algorithm = min(all_results, key=lambda x: x[1])
            print(f"🏆 Best performance: {best_algorithm[0]}")
            print(f"   Conflicts: {best_algorithm[1]}, Colors: {best_algorithm[2]}, Runtime: {best_algorithm[3]:.2f}s")

        return {
            "graph_file": "gc_250_9.txt",
            "vertices": len(graph.adj),
            "edges": sum(len(neighbors) for neighbors in graph.adj.values()) // 2,
            "greedy_colors": greedy_colors,
            "results": {
                "GA_TabuSearch": {"conflicts": best_conflicts, "colors": best_colors, "runtime": ts_time},
                "GA_AdaptiveRepair": {"conflicts": best_conflicts2, "colors": best_colors2, "runtime": adaptive_time},
                "MemeticGA": {"conflicts": best_conflicts3, "colors": best_colors3, "runtime": memetic_time},
                "GA_GreedyCustom": {"conflicts": best_conflicts4, "colors": best_colors4, "runtime": greedy_time}
            }
        }

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = test_gc250()
    
    if results:
        print("\n✅ Test completed successfully!")
        print("Results saved in memory for further analysis.")
    else:
        print("\n❌ Test failed!") 
