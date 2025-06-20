import os
from utils import parse_dimacs_graph
from hybrid_genetic_algorithms import GATabuSearch, GAAdaptiveRepair, MemeticGA, GAGreedyCustomCrossover
from base_genetic_algorithm import GeneticAlgorithm

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    
    # Test with a file known to have conflicts from previous runs
    file_name = "gc_50_9.txt" 
    file_path = os.path.join(data_dir, file_name)
    
    print("=" * 80)
    print(f"Testing ALL FOUR Hybrid Algorithms on {file_name}")
    print("=" * 80)

    try:
        graph = parse_dimacs_graph(file_path)

        # --- Test GA + DSATUR + Tabu Search ---
        print("\n\n--- METHOD 1: GA + DSATUR + Tabu Search ---")
        # From previous runs, dsatur gives 24 colors with 2 conflicts.
        # Let's try to solve it with 24 colors.
        num_colors = 24 
        ga_ts = GATabuSearch(
            graph=graph,
            population_size=50, # smaller for faster test
            num_colors=num_colors,
            tabu_iterations=1000, # More iterations for TS
            tabu_tenure=15
        )

        best_chromosome, best_fitness, best_conflicts, best_colors = ga_ts.run(generations=50)

        print("\n--- Final Result for GA+TS ---")
        print(f"  Best solution has {best_conflicts} conflicts.")
        print(f"  Colors used: {best_colors}")
        if best_conflicts == 0:
            print("  ✅ VALID SOLUTION FOUND!")
        else:
            print("  ❌ No valid solution found.")

        # --- Test GA + Constraint Repair + Adaptive Parameters ---
        print("\n\n--- METHOD 2: GA + Constraint Repair + Adaptive Parameters ---")
        ga_adaptive = GAAdaptiveRepair(
            graph=graph,
            population_size=50,
            num_colors=num_colors,
            base_mutation_rate=0.15,
            diversity_threshold=0.25
        )

        best_chromosome2, best_fitness2, best_conflicts2, best_colors2 = ga_adaptive.run(generations=50)

        print("\n--- Final Result for GA+Adaptive+Repair ---")
        print(f"  Best solution has {best_conflicts2} conflicts.")
        print(f"  Colors used: {best_colors2}")
        if best_conflicts2 == 0:
            print("  ✅ VALID SOLUTION FOUND!")
        else:
            print("  ❌ No valid solution found.")

        # --- Test Memetic GA ---
        print("\n\n--- METHOD 3: Memetic GA ---")
        memetic_ga = MemeticGA(
            graph=graph,
            population_size=50,
            num_colors=num_colors,
            local_search_type="tabu"
        )

        best_chromosome3, best_fitness3, best_conflicts3, best_colors3 = memetic_ga.run(generations=50)

        print("\n--- Final Result for Memetic GA ---")
        print(f"  Best solution has {best_conflicts3} conflicts.")
        print(f"  Colors used: {best_colors3}")
        if best_conflicts3 == 0:
            print("  ✅ VALID SOLUTION FOUND!")
        else:
            print("  ❌ No valid solution found.")

        # --- Test GA + Greedy + Custom Crossover ---
        print("\n\n--- METHOD 4: GA + Greedy + Custom Crossover ---")
        ga_greedy_custom = GAGreedyCustomCrossover(
            graph=graph,
            population_size=50,
            num_colors=num_colors,
            local_search_iterations=30
        )

        best_chromosome4, best_fitness4, best_conflicts4, best_colors4 = ga_greedy_custom.run(generations=50)

        print("\n--- Final Result for GA+Greedy+Custom ---")
        print(f"  Best solution has {best_conflicts4} conflicts.")
        print(f"  Colors used: {best_colors4}")
        if best_conflicts4 == 0:
            print("  ✅ VALID SOLUTION FOUND!")
        else:
            print("  ❌ No valid solution found.")

        # --- Comparison ---
        print("\n\n--- COMPARISON OF ALL FOUR METHODS ---")
        print(f"GA + DSATUR + Tabu Search:     {best_conflicts} conflicts, {best_colors} colors")
        print(f"GA + Adaptive + Repair:        {best_conflicts2} conflicts, {best_colors2} colors")
        print(f"Memetic GA:                    {best_conflicts3} conflicts, {best_colors3} colors")
        print(f"GA + Greedy + Custom Crossover: {best_conflicts4} conflicts, {best_colors4} colors")
        
        # Find the best algorithm
        valid_solutions = []
        if best_conflicts == 0:
            valid_solutions.append(("GA + DSATUR + Tabu Search", best_colors))
        if best_conflicts2 == 0:
            valid_solutions.append(("GA + Adaptive + Repair", best_colors2))
        if best_conflicts3 == 0:
            valid_solutions.append(("Memetic GA", best_colors3))
        if best_conflicts4 == 0:
            valid_solutions.append(("GA + Greedy + Custom Crossover", best_colors4))
        
        if len(valid_solutions) == 4:
            print("\n🎉 All four methods found valid solutions!")
            best_algorithm = min(valid_solutions, key=lambda x: x[1])
            print(f"🏆 Best algorithm: {best_algorithm[0]} ({best_algorithm[1]} colors)")
        elif len(valid_solutions) > 0:
            print(f"\n✅ {len(valid_solutions)} methods found valid solutions!")
            best_algorithm = min(valid_solutions, key=lambda x: x[1])
            print(f"🏆 Best algorithm: {best_algorithm[0]} ({best_algorithm[1]} colors)")
        else:
            print("\n❌ No method found a valid solution")
            # Find the one with least conflicts
            all_results = [
                ("GA + DSATUR + Tabu Search", best_conflicts, best_colors),
                ("GA + Adaptive + Repair", best_conflicts2, best_colors2),
                ("Memetic GA", best_conflicts3, best_colors3),
                ("GA + Greedy + Custom Crossover", best_conflicts4, best_colors4)
            ]
            best_algorithm = min(all_results, key=lambda x: x[1])
            print(f"🏆 Best performance: {best_algorithm[0]} ({best_algorithm[1]} conflicts, {best_algorithm[2]} colors)")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 
