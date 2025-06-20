import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_ga import HybridGA
from graph_loader import load_graph

if __name__ == "__main__":
    num_vertices, num_edges, adj_list = load_graph('gc_100_9.txt')
    mutation_rates = [0.05, 0.1, 0.2, 0.3, 0.5]
    mutation_strategies = ['classic', 'swap', 'inversion']
    best_fitness = float('inf')
    best_params = None
    best_solution = None
    print("Parametre taraması başlıyor...\n")
    for mut_type in mutation_strategies:
        for mut_rate in mutation_rates:
            print(f"Testing: mutation_strategy={mut_type}, mutation_rate={mut_rate}")
            ga = HybridGA(adj_list, num_vertices, num_colors=28, generations=400, verbose=False)
            ga.base_mutation_rate = mut_rate
            solution, fitness = ga.run(mutation_strategy=mut_type)
            print(f"  -> Fitness: {fitness} | Colors: {len(set(solution)) if solution else '-'}")
            if fitness < best_fitness:
                best_fitness = fitness
                best_params = (mut_type, mut_rate)
                best_solution = solution
    print("\nEn iyi parametreler:")
    print(f"Mutation strategy: {best_params[0]}, Mutation rate: {best_params[1]}")
    print(f"Best fitness: {best_fitness}")
    if best_solution and best_fitness == 0:
        print(f"Valid coloring with {len(set(best_solution))} colors!")
    else:
        print("No valid coloring found.") 
