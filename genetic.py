def fitness(chromosome: list[int], G: dict[int, list[int]]) -> float:
    """
    Lexicographic fitness:
      1) heavy penalty for any conflicts (force conflict-free)
      2) among conflict-free, minimize number of colors used
    """
    # Count edge-conflicts
    conflicts = 0
    for u, nbrs in G.items():
        for v in nbrs:
            if chromosome[u] == chromosome[v]:
                conflicts += 1
    conflicts //= 2  # each undirected edge counted twice

    used_colors = len(set(chromosome))
    if conflicts > 0:
        return conflicts * 1000 + used_colors
    return used_colors

def initialize_population(G: dict[int, list[int]], pop_size: int,
                         seed_ratio: float = 0.5) -> list[list[int]]:
    """
    Mix of random and heuristic seeds:
      - seed_ratio fraction from greedy_coloring and dsatur_coloring
      - rest random as before
    """
    import random
    from greedy import greedy_coloring, dsatur_coloring
    n = len(G)
    pop = []
    # heuristic seeds
    num_seeds = int(pop_size * seed_ratio)
    if num_seeds > 0:
        g = greedy_coloring(G)
        d = dsatur_coloring(G)
        # Convert dict values to lists in node order
        g_colors = [g[i] for i in range(n)]
        d_colors = [d[i] for i in range(n)]
        pop.extend([g_colors, d_colors])
        # if more seeds wanted, random perturbations
        for _ in range(num_seeds - 2):
            seed = g_colors if random.random() < 0.5 else d_colors
            random.shuffle(seed)
            pop.append(seed)
    # fill rest randomly
    for _ in range(pop_size - len(pop)):
        pop.append([random.randrange(n) for _ in range(n)])
    return pop

def tune_parameters(G: dict[int, list[int]], param_grid: dict) -> dict:
    """
    param_grid: e.g. {'pop_size':[50,100], 'mutation_rate':[0.05,0.1], ...}
    Runs GA for each combo, returns best-params dict.
    """
    import itertools, time
    best_score = float('inf')
    best_params = {}
    for combo in itertools.product(*param_grid.values()):
        params = dict(zip(param_grid.keys(), combo))
        start = time.time()
        chrom = ga_coloring(G, **params)
        score = fitness(chrom, G)
        dur = time.time() - start
        if score < best_score:
            best_score, best_params = score, params.copy()
    print("Tuning complete. Best score:", best_score, "with", best_params)
    return best_params

def ga_coloring(G: dict[int, list[int]], k: int, pop_size: int = 100, 
                generations: int = 100, mutation_rate: float = 0.1,
                seed_ratio: float = 0.5) -> dict[int, int]:
    """
    Genetic algorithm for graph coloring.
    Args:
        G: adjacency list representation of graph
        k: maximum number of colors allowed
        pop_size: size of population
        generations: number of generations to evolve
        mutation_rate: probability of mutation per gene
        seed_ratio: fraction of population to initialize with heuristic seeds
    Returns:
        dict mapping nodes to colors, or None if no solution found
    """
    import random
    import numpy as np
    
    n = len(G)
    
    def crossover(parent1: list[int], parent2: list[int]) -> list[int]:
        """Single-point crossover"""
        point = random.randint(0, n-1)
        return parent1[:point] + parent2[point:]
    
    def mutate(individual: list[int]) -> list[int]:
        """Mutate each gene with probability mutation_rate"""
        return [random.randint(0, k-1) if random.random() < mutation_rate else c 
                for c in individual]
    
    # Initialize population with heuristic seeds
    population = initialize_population(G, pop_size, seed_ratio)
    
    # Evolution loop
    for gen in range(generations):
        # Evaluate fitness
        fitnesses = [fitness(ind, G) for ind in population]
        best_idx = np.argmin(fitnesses)
        best_fitness = fitnesses[best_idx]
        
        # Print progress
        if gen % 10 == 0:
            print(f"Generation {gen}: best fitness = {best_fitness}")
        
        # Check if we found a solution
        if best_fitness < 1000:  # No conflicts
            return {i: c for i, c in enumerate(population[best_idx])}
        
        # Selection: tournament selection
        new_population = []
        for _ in range(pop_size):
            # Select two random individuals
            idx1, idx2 = random.sample(range(pop_size), 2)
            # Choose the better one
            parent1 = population[idx1 if fitnesses[idx1] < fitnesses[idx2] else idx2]
            # Repeat for second parent
            idx1, idx2 = random.sample(range(pop_size), 2)
            parent2 = population[idx1 if fitnesses[idx1] < fitnesses[idx2] else idx2]
            
            # Create child through crossover and mutation
            child = mutate(crossover(parent1, parent2))
            new_population.append(child)
        
        # Elitism: keep best individual
        new_population[0] = population[best_idx]
        population = new_population
    
    # If we get here, no solution found
    return None

if __name__ == "__main__":
    from parser import read_graph
    import time
    
    # Test on a small graph
    G = read_graph("gc_50_9.txt")
    
    # Define parameter grid for tuning
    param_grid = {
        'k': [9],
        'pop_size': [50, 100],
        'generations': [50, 100],
        'mutation_rate': [0.05, 0.1],
        'seed_ratio': [0.3, 0.5]
    }
    
    # Tune parameters
    print("Starting parameter tuning...")
    best_params = tune_parameters(G, param_grid)
    
    # Run with best parameters
    print("\nRunning with best parameters...")
    start = time.time()
    solution = ga_coloring(G, **best_params)
    t = time.time() - start
    
    if solution:
        colors = len(set(solution.values()))
        print(f"Found solution with {colors} colors in {t:.2f} seconds")
        print("Sample coloring:", dict(sorted(solution.items())[:5]))
    else:
        print("No solution found") 