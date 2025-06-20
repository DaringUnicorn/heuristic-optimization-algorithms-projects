import sys
import random
import matplotlib.pyplot as plt
import argparse
import os
import csv


def read_input(file=None):
    """
    Reads graph data from a file or stdin.
    First line: n_nodes, n_edges
    Next n_edges lines: u v
    Returns n_nodes, edges list.
    """
    if file is None:
        data = sys.stdin.read().strip().split()
    else:
        with open(file, 'r') as f:
            data = f.read().strip().split()
    it = iter(data)
    try:
        n_nodes = int(next(it))
        n_edges = int(next(it))
    except StopIteration:
        raise ValueError("Invalid input format")
    edges = []
    for _ in range(n_edges):
        u = int(next(it)); v = int(next(it))
        edges.append((u, v))
    return n_nodes, edges


def objective(chrom):
    """Number of colors used (colors are 0..k-1)."""
    return max(chrom) + 1


def fitness(chrom, edges, penalty_weight):
    """Objective + heavy penalty for each conflict."""
    conflicts = sum(1 for u, v in edges if chrom[u] == chrom[v])
    return objective(chrom) + penalty_weight * conflicts


def greedy_coloring(n_nodes, edges):
    coloring = [-1] * n_nodes
    adj = [[] for _ in range(n_nodes)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    for u in range(n_nodes):
        used = {coloring[v] for v in adj[u] if coloring[v] != -1}
        for c in range(n_nodes):
            if c not in used:
                coloring[u] = c
                break
    return coloring


def greedysat_coloring(n_nodes, edges):
    # Greedy coloring by saturation degree, but without full DSatur tie-breaking
    adj = [[] for _ in range(n_nodes)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    coloring = [-1] * n_nodes
    saturation = [0] * n_nodes
    neighbor_colors = [set() for _ in range(n_nodes)]
    uncolored = set(range(n_nodes))
    for _ in range(n_nodes):
        # Pick node with max saturation (break ties arbitrarily)
        u = max(uncolored, key=lambda x: saturation[x])
        used = {coloring[v] for v in adj[u] if coloring[v] != -1}
        for c in range(n_nodes):
            if c not in used:
                coloring[u] = c
                break
        for v in adj[u]:
            if coloring[u] not in neighbor_colors[v]:
                neighbor_colors[v].add(coloring[u])
                saturation[v] = len(neighbor_colors[v])
        uncolored.remove(u)
    return coloring


def init_population(pop_size, n_nodes, max_colors, edges=None, greedysat_seed=False):
    pop = []
    if greedysat_seed and edges is not None:
        greedysat = greedysat_coloring(n_nodes, edges)
        for i in range(len(greedysat)):
            if greedysat[i] >= max_colors:
                greedysat[i] = random.randrange(max_colors)
        pop.append(greedysat)
    while len(pop) < pop_size:
        pop.append([random.randrange(max_colors) for _ in range(n_nodes)])
    return pop


def tournament_select(pop, fits, k):
    """Tournament selection of size k."""
    contenders = random.sample(list(zip(pop, fits)), k)
    winner = min(contenders, key=lambda x: x[1])[0]
    return winner[:]


def one_point_crossover(p1, p2):
    n = len(p1)
    pt = random.randint(1, n-1)
    return p1[:pt] + p2[pt:]


def mutate(chrom, max_colors, current_mut_rate):
    for i in range(len(chrom)):
        if random.random() < current_mut_rate:
            chrom[i] = random.randrange(max_colors)


def better_local_search(chrom, edges, max_colors):
    # Try to swap colors between pairs of nodes to reduce the number of colors
    n = len(chrom)
    best = chrom[:]
    best_obj = objective(best)
    improved = False
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i+1, n):
                if best[i] != best[j]:
                    # Swap colors
                    best[i], best[j] = best[j], best[i]
                    if is_valid_coloring(best, edges):
                        obj = objective(best)
                        if obj < best_obj:
                            best_obj = obj
                            improved = True
                            changed = True
                        else:
                            # Undo swap
                            best[i], best[j] = best[j], best[i]
                    else:
                        # Undo swap
                        best[i], best[j] = best[j], best[i]
        # After one full pass, try to decrement colors as before
        for i in range(n):
            for c in range(best[i]-1, -1, -1):
                old = best[i]
                best[i] = c
                if all(best[u] != best[v] for u, v in edges):
                    if objective(best) < best_obj:
                        best_obj = objective(best)
                        improved = True
                        changed = True
                else:
                    best[i] = old
                    break
    return best if improved else None


def run_ga(n_nodes,
           edges,
           pop_size=200,
           max_gens=2000,
           max_colors=None,
           tournament_k=4,
           crossover_prob=0.9,
           base_mutation_rate=0.05,
           penalty_weight=None,
           stagnation_limit=50,
           mutation_factor=2.0,
           log_interval=100,
           long_stagnation=1000,
           greedysat_seed=False):
    if max_colors is None:
        max_colors = n_nodes
    if penalty_weight is None:
        penalty_weight = len(edges) * 100

    print(f"[GA] Starting: pop_size={pop_size}, max_gens={max_gens}, max_colors={max_colors}, tournament_k={tournament_k}, crossover_prob={crossover_prob}")
    population = init_population(pop_size, n_nodes, max_colors, edges, greedysat_seed)
    fitnesses = [fitness(ind, edges, penalty_weight) for ind in population]

    best_fit = min(fitnesses)
    best_ind = population[fitnesses.index(best_fit)][:]
    history = []
    gens_since_improve = 0
    restarts = 0

    for gen in range(max_gens):
        if gens_since_improve >= stagnation_limit:
            current_mut_rate = min(1.0, base_mutation_rate * mutation_factor)
            if gens_since_improve == stagnation_limit:
                print(f"[GA][Gen {gen}] Stagnation detected. Boosting mutation rate to {current_mut_rate}")
        else:
            current_mut_rate = base_mutation_rate

        history.append(best_fit)
        # Elitism: always keep the best individual
        new_pop = [best_ind[:]]

        while len(new_pop) < pop_size:
            p1 = tournament_select(population, fitnesses, tournament_k)
            p2 = tournament_select(population, fitnesses, tournament_k)
            if random.random() < crossover_prob:
                child = one_point_crossover(p1, p2)
            else:
                child = p1[:]
            mutate(child, max_colors, current_mut_rate)
            new_pop.append(child)

        population = new_pop
        fitnesses = [fitness(ind, edges, penalty_weight) for ind in population]
        gen_best = min(fitnesses)
        gen_best_ind = population[fitnesses.index(gen_best)][:]

        # Better local search: try swaps and decrements
        improved = False
        local_best = better_local_search(gen_best_ind, edges, max_colors)
        if local_best is not None:
            local_fit = fitness(local_best, edges, penalty_weight)
            if local_fit < gen_best:
                print(f"[GA][Gen {gen}] Better local search improved best fitness: {local_fit} (colors: {objective(local_best)})")
                gen_best = local_fit
                gen_best_ind = local_best
                improved = True

        if gen_best < best_fit:
            print(f"[GA][Gen {gen}] New best fitness: {gen_best} (colors: {objective(gen_best_ind)})")
            best_fit = gen_best
            best_ind = gen_best_ind
            gens_since_improve = 0
        else:
            gens_since_improve += 1

        if (gen + 1) % log_interval == 0 or gen == 0:
            print(f"[GA][Gen {gen+1}] Best fitness so far: {best_fit} (colors: {objective(best_ind)})")

        # Warn or restart after long stagnation
        if gens_since_improve >= long_stagnation:
            if long_stagnation < max_gens:
                print(f"[GA][Gen {gen}] Long stagnation detected. Restarting population from best with color shift.")
                restarts += 1
                population = [best_ind[:]]
                for _ in range(pop_size - 1):
                    shifted = best_ind[:]
                    # randomly shift a few nodes' colors
                    for _ in range(max(1, n_nodes // 10)):
                        idx = random.randrange(n_nodes)
                        shifted[idx] = random.randrange(max_colors)
                    population.append(shifted)
                fitnesses = [fitness(ind, edges, penalty_weight) for ind in population]
                gens_since_improve = 0
            else:
                print(f"[GA][Gen {gen}] WARNING: Stuck at local optimum for {long_stagnation} generations. No restart will be performed (long_stagnation >= max_gens). Consider lowering --long_stagnation if you want restarts.")

    print(f"[GA] Finished. Best fitness: {best_fit} (colors: {objective(best_ind)}), Restarts: {restarts}")
    return best_ind, history, restarts


def is_valid_coloring(chrom, edges):
    """Returns True if no adjacent nodes share the same color."""
    return all(chrom[u] != chrom[v] for u, v in edges)


def dsatur_coloring(n_nodes, edges):
    # Build adjacency list
    adj = [[] for _ in range(n_nodes)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    # Initialize
    coloring = [-1] * n_nodes
    saturation = [0] * n_nodes  # Number of different colors in neighborhood
    degrees = [len(adj[u]) for u in range(n_nodes)]
    uncolored = set(range(n_nodes))
    neighbor_colors = [set() for _ in range(n_nodes)]
    for _ in range(n_nodes):
        # Select vertex with highest saturation, break ties by degree
        max_sat = max(saturation[u] for u in uncolored)
        candidates = [u for u in uncolored if saturation[u] == max_sat]
        if len(candidates) > 1:
            u = max(candidates, key=lambda x: degrees[x])
        else:
            u = candidates[0]
        # Assign the smallest available color
        used = {coloring[v] for v in adj[u] if coloring[v] != -1}
        for c in range(n_nodes):
            if c not in used:
                coloring[u] = c
                break
        # Update saturation of neighbors
        for v in adj[u]:
            if coloring[u] not in neighbor_colors[v]:
                neighbor_colors[v].add(coloring[u])
                saturation[v] = len(neighbor_colors[v])
        uncolored.remove(u)
    return coloring


def main():
    parser = argparse.ArgumentParser(description="Genetic Algorithm for Graph Coloring with Adaptive Mutation")
    parser.add_argument('-f', '--file', type=str, default=None, help='Input file (default: stdin)')
    parser.add_argument('--pop_size', type=int, default=300, help='Population size (default: 300)')
    parser.add_argument('--max_gens', type=int, default=5000, help='Max generations (default: 5000)')
    parser.add_argument('--tournament_k', type=int, default=5, help='Tournament size (default: 5)')
    parser.add_argument('--base_mutation_rate', type=float, default=0.03, help='Base mutation rate (default: 0.03)')
    parser.add_argument('--stagnation_limit', type=int, default=100, help='Stagnation limit (default: 100)')
    parser.add_argument('--mutation_factor', type=float, default=3.0, help='Mutation factor (default: 3.0)')
    parser.add_argument('--save_plot', type=str, default=None, help='Path to save convergence plot (optional)')
    parser.add_argument('--save_result', type=str, default=None, help='Path to save coloring result (optional)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (default: 42)')
    parser.add_argument('--max_colors', type=int, default=None, help='Maximum number of colors allowed (default: n_nodes)')
    parser.add_argument('--long_stagnation', type=int, default=1000, help='Generations before restart (default: 1000)')
    parser.add_argument('--greedysat_seed', action='store_true', help='Include Greedy Saturation solution as a seed in the GA initial population')
    parser.add_argument('--crossover_prob', type=float, default=0.9, help='Probability of crossover between parents (default: 0.9)')
    args = parser.parse_args()

    random.seed(args.seed)
    n_nodes, edges = read_input(args.file)

    best_solution, history, restarts = run_ga(
        n_nodes,
        edges,
        pop_size=args.pop_size,
        max_gens=args.max_gens,
        tournament_k=args.tournament_k,
        crossover_prob=args.crossover_prob,
        base_mutation_rate=args.base_mutation_rate,
        stagnation_limit=args.stagnation_limit,
        mutation_factor=args.mutation_factor,
        log_interval=100,
        max_colors=args.max_colors if args.max_colors is not None else n_nodes,
        long_stagnation=args.long_stagnation,
        greedysat_seed=args.greedysat_seed
    )

    obj = objective(best_solution)
    valid = is_valid_coloring(best_solution, edges)

    print(f"Colors used: {obj}")
    print("Valid coloring:" if valid else "Invalid coloring!", "\n" + " ".join(map(str, best_solution)))

    if args.save_result:
        with open(args.save_result, 'w') as f:
            f.write(f"Colors used: {obj}\n")
            f.write("Valid coloring:\n" if valid else "Invalid coloring!\n")
            f.write(" ".join(map(str, best_solution)) + "\n")

    # Save to CSV if requested
    if args.save_csv:
        fieldnames = [
            'input_file', 'pop_size', 'max_gens', 'tournament_k', 'base_mutation_rate', 'stagnation_limit',
            'mutation_factor', 'max_colors', 'long_stagnation', 'greedy_seeds', 'seed',
            'best_colors', 'valid', 'restarts', 'generations', 'best_solution'
        ]
        row = {
            'input_file': args.file,
            'pop_size': args.pop_size,
            'max_gens': args.max_gens,
            'tournament_k': args.tournament_k,
            'base_mutation_rate': args.base_mutation_rate,
            'stagnation_limit': args.stagnation_limit,
            'mutation_factor': args.mutation_factor,
            'max_colors': args.max_colors if args.max_colors is not None else n_nodes,
            'long_stagnation': args.long_stagnation,
            'greedy_seeds': args.greedy_seeds,
            'seed': args.seed,
            'best_colors': obj,
            'valid': valid,
            'restarts': restarts,
            'generations': len(history),
            'best_solution': " ".join(map(str, best_solution))
        }
        with open(args.save_csv, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)

    # plot convergence
    plt.figure()
    plt.plot(history)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness (penalized)')
    plt.title('GA Convergence with Adaptive Mutation')
    plt.grid(True)
    plt.tight_layout()
    if args.save_plot:
        plt.savefig(args.save_plot)
        print(f"Plot saved to {args.save_plot}")
    else:
        plt.show()

if __name__ == "__main__":
    main()