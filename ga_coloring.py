"""
ga_coloring.py
Genetic Algorithm for Graph Coloring
Advanced Features: Elitism + Hybridization (GA + SA) + Lexicographic Fitness + Heuristic Seeding + Parameter Tuning
"""

import random
import math
from parser import read_graph
from greedy import greedy_coloring, dsatur_coloring

def fitness(chromosome: list[int], G: dict[int, list[int]]) -> float:
    """
    Lexicographic fitness:
      1) heavy penalty for any conflicts (force conflict-free)
      2) among conflict-free, minimize number of colors used
    Lower is better.
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

def initialize_population(
    G: dict[int, list[int]],
    pop_size: int,
    seed_ratio: float = 0.5
) -> list[list[int]]:
    """
    Mix of random and heuristic seeds:
      - seed_ratio fraction from greedy_coloring and dsatur_coloring
      - rest random as before
    """
    n = len(G)
    pop: list[list[int]] = []
    num_seeds = int(pop_size * seed_ratio)
    # Heuristic seeds
    if num_seeds >= 2:
        g = greedy_coloring(G)
        d = dsatur_coloring(G)
        # Convert dict to list in index order
        g_list = [g[i] for i in range(n)]
        d_list = [d[i] for i in range(n)]
        pop.extend([g_list, d_list])
        for _ in range(num_seeds - 2):
            seed = g_list.copy() if random.random() < 0.5 else d_list.copy()
            random.shuffle(seed)
            pop.append(seed)
    # Fill rest randomly
    while len(pop) < pop_size:
        pop.append([random.randrange(n) for _ in range(n)])
    return pop

def tournament_selection(
    pop: list[list[int]],
    fits: list[float],
    k: int
) -> list[int]:
    """
    k-tournament selection: pick k random individuals, return the best.
    """
    candidates = random.sample(list(zip(pop, fits)), k)
    winner = min(candidates, key=lambda x: x[1])[0]
    return winner

def crossover(
    parent1: list[int],
    parent2: list[int]
) -> tuple[list[int], list[int]]:
    """
    Single-point crossover.
    """
    n = len(parent1)
    pt = random.randrange(1, n)
    return (
        parent1[:pt] + parent2[pt:],
        parent2[:pt] + parent1[pt:]
    )

def mutate(
    chrom: list[int],
    mutation_rate: float
) -> None:
    """
    Randomly reassign gene with mutation_rate.
    """
    n = len(chrom)
    for i in range(n):
        if random.random() < mutation_rate:
            chrom[i] = random.randrange(n)

def simulated_annealing(
    chrom: list[int],
    G: dict[int, list[int]],
    initial_temp: float,
    cooling_rate: float,
    sa_steps: int
) -> list[int]:
    """
    Local improvement: small SA to reduce conflicts/colors.
    """
    best = chrom.copy()
    best_fit = fitness(best, G)
    temp = initial_temp
    for _ in range(sa_steps):
        i, j = random.sample(range(len(chrom)), 2)
        neighbor = best.copy()
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        fit_n = fitness(neighbor, G)
        if fit_n < best_fit or random.random() < math.exp(-(fit_n - best_fit)/temp):
            best, best_fit = neighbor, fit_n
        temp *= cooling_rate
    return best

def replace_population(
    pop: list[list[int]],
    offspring: list[list[int]],
    fits: list[float],
    elitism_rate: float
) -> list[list[int]]:
    """
    Keep the top-elitism_rate fraction of old population, fill rest with best offspring.
    """
    pop_size = len(pop)
    elite_count = int(elitism_rate * pop_size)
    # sort old pop by fitness ascending
    sorted_old = [chrom for chrom, _ in sorted(zip(pop, fits), key=lambda x: x[1])]
    return sorted_old[:elite_count] + offspring[:pop_size - elite_count]

def ga_coloring(
    G: dict[int, list[int]],
    pop_size: int = 100,
    generations: int = 200,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.1,
    elitism_rate: float = 0.1,
    sa_temp: float = 1.0,
    sa_cooling: float = 0.95,
    sa_steps: int = 10,
    tournament_k: int = 3
) -> list[int]:
    """
    Run GA with elitism and hybrid SA.
    Returns best chromosome as a list of colors.
    """
    # Initialize
    population = initialize_population(G, pop_size, seed_ratio=0.5)
    fits = [fitness(ind, G) for ind in population]
    best_chrom = min(population, key=lambda c: fitness(c, G))
    # Evolve
    for gen in range(generations):
        offspring: list[list[int]] = []
        for _ in range(pop_size // 2):
            # Select parents
            p1 = tournament_selection(population, fits, tournament_k)
            p2 = tournament_selection(population, fits, tournament_k)
            # Crossover
            if random.random() < crossover_rate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()
            # Mutation
            mutate(c1, mutation_rate)
            mutate(c2, mutation_rate)
            # Hybrid SA
            c1 = simulated_annealing(c1, G, sa_temp, sa_cooling, sa_steps)
            c2 = simulated_annealing(c2, G, sa_temp, sa_cooling, sa_steps)
            offspring.extend([c1, c2])
        # Replacement + elitism
        population = replace_population(population, offspring, fits, elitism_rate)
        fits = [fitness(ind, G) for ind in population]
        # Track best
        current_best = min(population, key=lambda c: fitness(c, G))
        if fitness(current_best, G) < fitness(best_chrom, G):
            best_chrom = current_best
    return best_chrom

def tune_parameters(
    G: dict[int, list[int]],
    param_grid: dict
) -> dict:
    """
    param_grid: e.g. {'pop_size':[50,100], 'mutation_rate':[0.05,0.1], ...}
    Runs GA for each combo, returns best-params dict.
    """
    import itertools, time
    best_score = float('inf')
    best_params: dict = {}
    for combo in itertools.product(*param_grid.values()):
        params = dict(zip(param_grid.keys(), combo))
        start = time.time()
        chrom = ga_coloring(G, **params)
        score = fitness(chrom, G)
        if score < best_score:
            best_score, best_params = score, params.copy()
    print("Tuning complete. Best score:", best_score, "with", best_params)
    return best_params

if __name__ == "__main__":
    # Quick example
    G = read_graph("gc_50_9.txt")
    best = ga_coloring(G)
    print("Best coloring found:", best)
