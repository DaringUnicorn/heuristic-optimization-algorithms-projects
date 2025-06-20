import os
from utils import parse_dimacs_graph
from base_genetic_algorithm import GeneticAlgorithm 
from hybrid_genetic_algorithms import GATabuSearch, GAAdaptiveRepair, MemeticGA, GAGreedyCustomCrossover, GreedyInitializer 
import time

# Experiment parameters
generations_list = [100, 500, 1000]
num_colors_list = [7, 8, 9, 10]
population_sizes = [50, 100, 200]
initializers = ["random", "dsatur", "greedy", "mixed"]

file_name = "gc_50_9.txt"
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "..", "data", file_name)

print(f"Loading graph from: {file_path}")
graph = parse_dimacs_graph(file_path)
print("Graph loaded successfully!")
print(graph)
print("-" * 50)

results = []

total_runs = len(generations_list) * len(num_colors_list) * len(population_sizes) * len(initializers)
run_count = 0

for generations in generations_list:
    for num_colors in num_colors_list:
        for pop_size in population_sizes:
            for initializer in initializers:
                run_count += 1
                print(f"\n[Run {run_count}/{total_runs}] Gen:{generations}, Colors:{num_colors}, Pop:{pop_size}, Init:{initializer}")
                start_time = time.time()
                ga = GeneticAlgorithm(
                    graph=graph,
                    population_size=pop_size,
                    num_colors=num_colors,
                    initializer=initializer
                )
                best_chromosome, best_fitness, best_conflicts, best_colors = ga.run(generations=generations)
                elapsed = time.time() - start_time
                results.append({
                    "generations": generations,
                    "num_colors": num_colors,
                    "population": pop_size,
                    "initializer": initializer,
                    "fitness": best_fitness,
                    "conflicts": best_conflicts,
                    "colors_used": best_colors,
                    "time": elapsed
                })
                print(f"Result: Fitness={best_fitness}, Conflicts={best_conflicts}, Colors={best_colors}, Time={elapsed:.2f}s")

# Print summary table
print("\nSUMMARY TABLE:")
print(f"{'Gen':>5} {'Col':>4} {'Pop':>4} {'Init':>8} {'Fit':>8} {'Conf':>5} {'Used':>5} {'Time':>7}")
for r in results:
    print(f"{r['generations']:5d} {r['num_colors']:4d} {r['population']:4d} {r['initializer']:>8} {r['fitness']:8.2f} {r['conflicts']:5d} {r['colors_used']:5d} {r['time']:7.2f}") 
