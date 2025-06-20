import random
from heuristics import dsatur_coloring

def calculate_fitness(chromosome, adj_list):
    """
    Calculates the fitness of a chromosome.
    Fitness is defined as the number of conflicting edges. A fitness of 0 is a valid solution.
    """
    conflicts = 0
    for u in adj_list:
        for v in adj_list[u]:
            if u < v:  # To avoid double counting
                if chromosome[u] == chromosome[v]:
                    conflicts += 1
    return conflicts

def local_search_improvement(chromosome, adj_list, num_colors):
    """
    Improves a chromosome by performing local search.
    It identifies conflicting nodes and tries to change their color to resolve the conflict.
    """
    conflicting_nodes = []
    for u in adj_list:
        for v in adj_list[u]:
            if u < v and chromosome[u] == chromosome[v]:
                conflicting_nodes.append(u)
                conflicting_nodes.append(v)
    
    # Iterate over a shuffled list of unique conflicting nodes
    for node in random.sample(list(set(conflicting_nodes)), len(set(conflicting_nodes))):
        current_color = chromosome[node]
        neighbor_colors = {chromosome[neighbor] for neighbor in adj_list[node]}

        # Try to find a new color that resolves the conflict
        best_color = current_color
        min_conflicts = float('inf')

        for color in range(1, num_colors + 1):
            if color != current_color:
                # Count conflicts if we change to this color
                new_conflicts = sum(1 for neighbor in adj_list[node] if chromosome[neighbor] == color)
                if new_conflicts < min_conflicts:
                    min_conflicts = new_conflicts
                    best_color = color
        
        # If a better color is found (less conflicts), apply it
        current_conflicts = sum(1 for neighbor in adj_list[node] if chromosome[neighbor] == current_color)
        if min_conflicts < current_conflicts:
            chromosome[node] = best_color
            
    return chromosome

def run_memetic_algorithm(adj_list, num_vertices, num_colors, verbose=True):
    """
    Main function to run the Memetic Algorithm for graph coloring.
    """
    if verbose:
        print("\nRunning Memetic Algorithm (GA + Local Search)...")
    
    # --- 1. GA Parameters (More Aggressive Search) ---
    population_size = 200
    generations = 500
    mutation_rate = 0.2
    crossover_rate = 0.85
    tournament_size = 5
    local_search_rate = 0.2 # Apply local search to the top 20%
    
    # The number of colors is now passed as a parameter.
    # We no longer need to run DSatur here just for the color count.
    
    # --- 2. Initialization ---
    population = []
    
    # We can still use a DSatur solution if we want, but it might use more colors
    # than we are currently targeting. For now, let's start with a fully random population.
    for _ in range(population_size):
        chromosome = [random.randint(1, num_colors) for _ in range(num_vertices)]
        population.append(chromosome)

    # --- 3. Main GA Loop ---
    best_solution_overall = None
    best_fitness_overall = float('inf')

    for gen in range(generations):
        fitness_scores = [calculate_fitness(chromo, adj_list) for chromo in population]

        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1])
        population = [item[0] for item in sorted_population]
        fitness_scores = [item[1] for item in sorted_population]
        
        current_best_fitness = fitness_scores[0]
        if current_best_fitness < best_fitness_overall:
            best_fitness_overall = current_best_fitness
            best_solution_overall = population[0]
            if verbose:
                print(f"Generation {gen+1}/{generations} | Best Fitness: {best_fitness_overall}")

        if best_fitness_overall == 0:
            if verbose:
                print("Found a valid coloring!")
            break

        # --- 4. Elitism and Selection ---
        new_population = []
        elitism_count = int(population_size * 0.1) # Keep top 10%
        new_population.extend(population[:elitism_count])

        # Apply Local Search to some of the elite individuals
        for i in range(int(elitism_count * local_search_rate)):
             new_population[i] = local_search_improvement(new_population[i], adj_list, num_colors)
            
        # --- 5. Crossover and Mutation ---
        while len(new_population) < population_size:
            parents = []
            for _ in range(2):
                tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
                winner = min(tournament, key=lambda x: x[1])[0]
                parents.append(winner)

            if random.random() < crossover_rate:
                point = random.randint(1, num_vertices - 1)
                child1 = parents[0][:point] + parents[1][point:]
                child2 = parents[1][:point] + parents[0][point:]
            else:
                child1, child2 = parents[0][:], parents[1][:]

            for child in [child1, child2]:
                for i in range(num_vertices):
                    if random.random() < mutation_rate:
                        child[i] = random.randint(1, num_colors)
                new_population.append(child)
        
        population = new_population[:population_size]
    
    if verbose:
        print("\nMA run finished.")
        if best_fitness_overall == 0:
            final_colors = len(set(best_solution_overall))
            print(f"Found a valid solution with {final_colors} colors.")
        else:
            print(f"Could not find a valid solution. Best attempt had {best_fitness_overall} conflicts.")

    return best_solution_overall 
