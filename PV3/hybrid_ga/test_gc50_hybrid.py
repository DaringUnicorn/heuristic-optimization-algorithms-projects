import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hybrid_ga import HybridGA
from graph_loader import load_graph

def adaptive_param_search(graph_file, num_colors, generations=1000):
    num_vertices, num_edges, adj_list = load_graph(graph_file)
    mutation_rates = [0.05, 0.1, 0.2, 0.3, 0.5]
    mutation_strategies = ['classic', 'swap', 'inversion']
    best_fitness = float('inf')
    best_params = None
    best_solution = None
    stuck_counter = 0
    print(f"\nTesting {graph_file} with {num_colors} colors and {generations} generations...")
    for mut_type in mutation_strategies:
        for mut_rate in mutation_rates:
            print(f"Testing: mutation_strategy={mut_type}, mutation_rate={mut_rate}")
            ga = HybridGA(adj_list, num_vertices, num_colors=num_colors, generations=generations, verbose=False)
            ga.base_mutation_rate = mut_rate
            solution, fitness = ga.run(mutation_strategy=mut_type)
            print(f"  -> Fitness: {fitness} | Colors: {len(set(solution)) if solution else '-'}")
            if fitness < best_fitness:
                best_fitness = fitness
                best_params = (mut_type, mut_rate)
                best_solution = solution
            if fitness > 0:
                stuck_counter += 1
                if stuck_counter > 3:
                    print("  -> Stuck in local optimum, increasing mutation rates and generations!")
                    mutation_rates = [0.3, 0.5, 0.7]
                    generations = int(generations * 1.5)
    print("\nBest parameters:")
    print(f"Mutation strategy: {best_params[0]}, Mutation rate: {best_params[1]}")
    print(f"Best fitness: {best_fitness}")
    if best_solution and best_fitness == 0:
        print(f"Valid coloring with {len(set(best_solution))} colors!")
    else:
        print("No valid coloring found.")

if __name__ == "__main__":
    adaptive_param_search('gc_50_9.txt', num_colors=22, generations=1000) 
