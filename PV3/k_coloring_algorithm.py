#!/usr/bin/env python3
"""
TRUE K-COLORING Algorithm
This enforces the k-color constraint DURING the GA process, not just at validation.
"""

import random
from graph_loader import load_graph
from heuristics import dsatur_coloring, welsh_powell_coloring, smallest_last_coloring

def calculate_fitness_k_coloring(chromosome, adj_list, k):
    """
    Fitness function for k-coloring:
    - Primary: Number of conflicting edges
    - Secondary: Penalty for using more than k colors
    """
    conflicts = 0
    for u in adj_list:
        for v in adj_list[u]:
            if u < v and chromosome[u] == chromosome[v]:
                conflicts += 1
    
    # Heavy penalty for using more than k colors
    colors_used = len(set(chromosome))
    color_penalty = max(0, colors_used - k) * 1000
    
    return conflicts + color_penalty

def enforce_k_constraint(chromosome, k):
    """
    Force chromosome to use only colors 1 to k
    """
    return [(color - 1) % k + 1 for color in chromosome]

def k_coloring_crossover(parent1, parent2, adj_list, k):
    """
    K-coloring aware crossover
    """
    num_vertices = len(parent1)
    child = [0] * num_vertices
    
    for vertex in range(num_vertices):
        # Choose color from parent that causes fewer conflicts
        # and respects k constraint
        color1 = parent1[vertex]
        color2 = parent2[vertex]
        
        # Ensure colors are within k range
        color1 = ((color1 - 1) % k) + 1
        color2 = ((color2 - 1) % k) + 1
        
        # Count conflicts for each choice
        neighbors = adj_list.get(vertex, [])
        conflicts1 = sum(1 for n in neighbors if n < vertex and child[n] == color1)
        conflicts2 = sum(1 for n in neighbors if n < vertex and child[n] == color2)
        
        if conflicts1 <= conflicts2:
            child[vertex] = color1
        else:
            child[vertex] = color2
    
    return child

def k_coloring_mutation(chromosome, k, mutation_rate=0.15):
    """
    Mutation that respects k constraint
    """
    mutated = chromosome[:]
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = random.randint(1, k)
    return mutated

def smart_k_coloring_initialization(adj_list, num_vertices, k, population_size=100):
    """
    Smart population initialization for k-coloring
    """
    population = []
    
    # Try to get a good base solution from heuristics
    try:
        heuristic_k, heuristic_solution = dsatur_coloring(adj_list)
        if heuristic_k <= k:
            # If heuristic uses ≤ k colors, use it as base
            base_solution = [heuristic_solution.get(i, 1) for i in range(num_vertices)]
            population.append(base_solution)
    except:
        pass
    
    # Generate diverse solutions
    while len(population) < population_size:
        # Random k-coloring
        chromosome = [random.randint(1, k) for _ in range(num_vertices)]
        population.append(chromosome)
    
    return population

def run_true_k_coloring_ga(adj_list, num_vertices, k, max_generations=500, verbose=True):
    """
    Genetic Algorithm specifically designed for k-coloring
    """
    if verbose:
        print(f"\n🎯 TRUE K-COLORING GA for k={k}")
        print("=" * 50)
    
    # Parameters
    population_size = 150
    mutation_rate = 0.15
    crossover_rate = 0.8
    tournament_size = 5
    elite_size = int(population_size * 0.1)
    
    # Initialize population
    population = smart_k_coloring_initialization(adj_list, num_vertices, k, population_size)
    
    best_solution = None
    best_fitness = float('inf')
    stagnation = 0
    
    for generation in range(max_generations):
        # Evaluate fitness
        fitness_scores = []
        for chromo in population:
            # Enforce k constraint
            chromo = enforce_k_constraint(chromo, k)
            fitness = calculate_fitness_k_coloring(chromo, adj_list, k)
            fitness_scores.append(fitness)
        
        # Sort by fitness
        sorted_pop = sorted(zip(population, fitness_scores), key=lambda x: x[1])
        population = [item[0] for item in sorted_pop]
        fitness_scores = [item[1] for item in sorted_pop]
        
        # Track best solution
        current_best = fitness_scores[0]
        if current_best < best_fitness:
            best_fitness = current_best
            best_solution = population[0][:]
            stagnation = 0
            if verbose and generation % 20 == 0:
                colors_used = len(set(best_solution))
                print(f"Generation {generation}: fitness={best_fitness}, colors_used={colors_used}")
        else:
            stagnation += 1
        
        # Check if we found a valid k-coloring
        if best_fitness == 0:
            colors_used = len(set(best_solution))
            if verbose:
                print(f"🎉 FOUND VALID {k}-COLORING at generation {generation}!")
                print(f"   Solution uses {colors_used} distinct colors")
            break
        
        # Early stopping if stagnant
        if stagnation > 100:
            if verbose:
                print(f"Stopping early due to stagnation at generation {generation}")
            break
        
        # Create new generation
        new_population = []
        
        # Elitism
        new_population.extend([enforce_k_constraint(ind[:], k) for ind in population[:elite_size]])
        
        # Crossover and mutation
        while len(new_population) < population_size:
            # Tournament selection
            parent1 = min(random.sample(list(zip(population, fitness_scores)), tournament_size), 
                         key=lambda x: x[1])[0]
            parent2 = min(random.sample(list(zip(population, fitness_scores)), tournament_size), 
                         key=lambda x: x[1])[0]
            
            # Crossover
            if random.random() < crossover_rate:
                child = k_coloring_crossover(parent1, parent2, adj_list, k)
            else:
                child = parent1[:]
            
            # Mutation
            child = k_coloring_mutation(child, k, mutation_rate)
            
            # Ensure k constraint
            child = enforce_k_constraint(child, k)
            
            new_population.append(child)
        
        population = new_population[:population_size]
    
    # Final validation
    if best_solution:
        best_solution = enforce_k_constraint(best_solution, k)
        final_fitness = calculate_fitness_k_coloring(best_solution, adj_list, k)
        colors_used = len(set(best_solution))
        
        if verbose:
            print(f"\n📊 FINAL RESULT:")
            print(f"   Best fitness: {final_fitness}")
            print(f"   Colors used: {colors_used}")
            print(f"   Valid {k}-coloring: {final_fitness == 0 and colors_used <= k}")
        
        return best_solution if final_fitness == 0 and colors_used <= k else None
    
    return None

def test_true_k_coloring():
    """
    Test the true k-coloring algorithm on gc_50_9.txt
    """
    print("🚀 TESTING TRUE K-COLORING ALGORITHM")
    print("=" * 60)
    
    # Load graph
    num_vertices, num_edges, graph = load_graph('gc_50_9.txt')
    print(f"Graph: {num_vertices} vertices, {num_edges} edges")
    
    # Get baseline
    k_dsatur, _ = dsatur_coloring(graph)
    print(f"DSatur baseline: {k_dsatur} colors")
    
    # Test our true k-coloring algorithm
    print(f"\n🎯 Testing True K-Coloring Algorithm...")
    
    # Try to improve upon DSatur
    for k_target in range(k_dsatur - 1, max(k_dsatur - 5, 1), -1):
        print(f"\n--- Attempting k={k_target} ---")
        
        solution = run_true_k_coloring_ga(graph, num_vertices, k_target, max_generations=300, verbose=True)
        
        if solution:
            actual_colors = len(set(solution))
            conflicts = sum(1 for u in graph for v in graph[u] 
                          if u < v and solution[u] == solution[v])
            
            print(f"🎉 SUCCESS! Found valid {k_target}-coloring")
            print(f"   Uses {actual_colors} distinct colors")
            print(f"   Conflicts: {conflicts}")
            
            # Verify it's truly valid
            if conflicts == 0 and actual_colors <= k_target:
                print(f"✅ VERIFIED: True {k_target}-coloring achieved!")
                return k_target
            else:
                print(f"❌ VERIFICATION FAILED")
        else:
            print(f"❌ Failed to find {k_target}-coloring")
            break
    
    print(f"\n📊 CONCLUSION: Could not improve upon DSatur's {k_dsatur} colors")
    return k_dsatur

if __name__ == "__main__":
    test_true_k_coloring() 
