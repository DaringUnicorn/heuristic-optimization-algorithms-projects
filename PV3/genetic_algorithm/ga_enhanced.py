import random
from heuristics import dsatur_coloring, get_diverse_initial_solutions

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

def kempe_chain_search(chromosome, adj_list, max_attempts=50):
    """
    Advanced local search using Kempe chains.
    A Kempe chain is a connected component in the subgraph induced by vertices of two colors.
    """
    num_vertices = len(chromosome)
    colors_used = set(chromosome)
    improved = False
    
    for attempt in range(max_attempts):
        # Pick two different colors randomly
        if len(colors_used) < 2:
            break
            
        color1, color2 = random.sample(list(colors_used), 2)
        
        # Find all vertices with these colors
        vertices_c1 = [v for v in range(num_vertices) if chromosome[v] == color1]
        vertices_c2 = [v for v in range(num_vertices) if chromosome[v] == color2]
        
        if not vertices_c1 or not vertices_c2:
            continue
        
        # Build the subgraph with only these two colors
        subgraph_vertices = set(vertices_c1 + vertices_c2)
        
        # Find connected components in this 2-color subgraph
        visited = set()
        
        for start_vertex in subgraph_vertices:
            if start_vertex in visited:
                continue
                
            # BFS to find the connected component (Kempe chain)
            component = []
            queue = [start_vertex]
            visited.add(start_vertex)
            
            while queue:
                current = queue.pop(0)
                component.append(current)
                
                for neighbor in adj_list.get(current, []):
                    if neighbor in subgraph_vertices and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            if len(component) > 1:
                # Try swapping colors in this Kempe chain
                original_fitness = calculate_fitness(chromosome, adj_list)
                
                # Swap colors in the component
                for vertex in component:
                    if chromosome[vertex] == color1:
                        chromosome[vertex] = color2
                    else:
                        chromosome[vertex] = color1
                
                new_fitness = calculate_fitness(chromosome, adj_list)
                
                if new_fitness <= original_fitness:
                    # Keep the improvement
                    improved = True
                    if new_fitness == 0:  # Found valid solution
                        return chromosome
                else:
                    # Revert the change
                    for vertex in component:
                        if chromosome[vertex] == color1:
                            chromosome[vertex] = color2
                        else:
                            chromosome[vertex] = color1
    
    return chromosome

def tabu_search_refinement(chromosome, adj_list, max_iterations=100, tabu_length=20):
    """
    Tabu Search to refine the solution further.
    """
    current_solution = chromosome[:]
    best_solution = chromosome[:]
    current_fitness = calculate_fitness(current_solution, adj_list)
    best_fitness = current_fitness
    
    tabu_list = []
    
    for iteration in range(max_iterations):
        if current_fitness == 0:
            break
            
        best_move = None
        best_move_fitness = float('inf')
        
        # Generate neighborhood by changing color of conflicting vertices
        conflicting_vertices = []
        for u in adj_list:
            for v in adj_list[u]:
                if u < v and current_solution[u] == current_solution[v]:
                    conflicting_vertices.extend([u, v])
        
        conflicting_vertices = list(set(conflicting_vertices))
        
        if not conflicting_vertices:
            break
            
        # Try different color changes for conflicting vertices
        for vertex in conflicting_vertices[:min(10, len(conflicting_vertices))]:
            current_color = current_solution[vertex]
            neighbor_colors = {current_solution[neighbor] for neighbor in adj_list.get(vertex, [])}
            
            for new_color in range(1, max(current_solution) + 2):
                if new_color != current_color:
                    move = (vertex, current_color, new_color)
                    
                    # Skip if move is tabu (unless it leads to improvement)
                    if move in tabu_list:
                        continue
                    
                    # Apply move temporarily
                    current_solution[vertex] = new_color
                    move_fitness = calculate_fitness(current_solution, adj_list)
                    
                    if move_fitness < best_move_fitness:
                        best_move = move
                        best_move_fitness = move_fitness
                    
                    # Revert move
                    current_solution[vertex] = current_color
        
        if best_move is None:
            break
            
        # Apply best move
        vertex, old_color, new_color = best_move
        current_solution[vertex] = new_color
        current_fitness = best_move_fitness
        
        # Update tabu list
        tabu_list.append(best_move)
        if len(tabu_list) > tabu_length:
            tabu_list.pop(0)
        
        # Update best solution
        if current_fitness < best_fitness:
            best_fitness = current_fitness
            best_solution = current_solution[:]
    
    return best_solution

def conflict_aware_crossover(parent1, parent2, adj_list):
    """
    Intelligent crossover that considers graph structure.
    """
    num_vertices = len(parent1)
    child = [0] * num_vertices
    
    # For each vertex, choose the color from the parent that causes fewer conflicts
    for vertex in range(num_vertices):
        color1 = parent1[vertex]
        color2 = parent2[vertex]
        
        # Count conflicts for each color choice
        conflicts1 = sum(1 for neighbor in adj_list.get(vertex, []) 
                        if neighbor < vertex and parent1[neighbor] == color1)
        conflicts2 = sum(1 for neighbor in adj_list.get(vertex, []) 
                        if neighbor < vertex and parent2[neighbor] == color2)
        
        # Choose the color with fewer conflicts, with some randomness
        if conflicts1 < conflicts2:
            child[vertex] = color1
        elif conflicts2 < conflicts1:
            child[vertex] = color2
        else:
            child[vertex] = random.choice([color1, color2])
    
    return child

def run_enhanced_memetic_algorithm(adj_list, num_vertices, num_colors, verbose=True):
    """
    Main function to run the Memetic Algorithm for graph coloring
    with advanced heuristics and Kempe chain local search.
    """
    if verbose:
        print("\nRunning ADVANCED Memetic Algorithm (Multiple Heuristics + Kempe Chains + Smart Crossover)...")
    
    # --- 1. GA Parameters ---
    population_size = 150
    generations = 800
    base_mutation_rate = 0.15
    crossover_rate = 0.9
    tournament_size = 7
    kempe_search_rate = 0.3  # Apply Kempe chain search to top 30%
    
    # --- 2. Smart Population Initialization ---
    population = []
    
    # Get diverse initial solutions from multiple heuristics
    diverse_solutions = get_diverse_initial_solutions(adj_list, num_solutions=10)
    
    for solution_dict in diverse_solutions[:min(10, len(diverse_solutions))]:
        # Convert to chromosome format
        chromosome = [solution_dict.get(i, 1) for i in range(num_vertices)]
        # Remap colors to fit within num_colors
        unique_colors = list(set(chromosome))
        if num_colors > 0:
            color_map = {old_color: (i % num_colors) + 1 for i, old_color in enumerate(unique_colors)}
            chromosome = [color_map[color] for color in chromosome]
        population.append(chromosome)
    
    # Fill rest with random chromosomes
    while len(population) < population_size:
        chromosome = [random.randint(1, num_colors) for _ in range(num_vertices)]
        population.append(chromosome)

    # --- 3. Advanced GA Loop ---
    best_solution_overall = None
    best_fitness_overall = float('inf')
    stagnation_counter = 0
    current_mutation_rate = base_mutation_rate

    for gen in range(generations):
        # Evaluate fitness
        fitness_scores = [calculate_fitness(chromo, adj_list) for chromo in population]
        
        # Sort population by fitness
        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1])
        population = [item[0] for item in sorted_population]
        fitness_scores = [item[1] for item in sorted_population]
        
        current_best_fitness = fitness_scores[0]
        if current_best_fitness < best_fitness_overall:
            best_fitness_overall = current_best_fitness
            best_solution_overall = population[0][:]
            stagnation_counter = 0
            current_mutation_rate = base_mutation_rate
            if verbose:
                print(f"Generation {gen+1}/{generations} | Best Fitness: {best_fitness_overall}")
        else:
            stagnation_counter += 1
        
        # Adaptive mutation
        if stagnation_counter >= 30:
            current_mutation_rate = min(0.5, base_mutation_rate * 2)
            if verbose and stagnation_counter % 30 == 0:
                print(f"Stagnation detected! Increasing mutation rate to {current_mutation_rate}")
        
        if best_fitness_overall == 0:
            if verbose:
                print("Found a valid coloring!")
            break

        # --- 4. Advanced Local Search with Kempe Chains ---
        kempe_count = int(population_size * kempe_search_rate)
        for i in range(min(kempe_count, len(population))):
            population[i] = kempe_chain_search(population[i][:], adj_list)

        # --- 5. Tabu Search Refinement (every 50 generations) ---
        if gen > 0 and gen % 50 == 0 and best_solution_overall is not None:
            if verbose:
                print(f"Applying Tabu Search refinement at generation {gen+1}")
            refined_solution = tabu_search_refinement(best_solution_overall, adj_list)
            refined_fitness = calculate_fitness(refined_solution, adj_list)
            if refined_fitness < best_fitness_overall:
                best_fitness_overall = refined_fitness
                best_solution_overall = refined_solution
                if verbose:
                    print(f"Tabu Search improved solution to fitness: {best_fitness_overall}")

        # --- 6. Multi-restart mechanism (if severely stuck) ---
        if stagnation_counter >= 100:
            if verbose:
                print(f"Severe stagnation detected! Restarting with new diverse population...")
            # Keep only the best 20% and generate new diverse solutions
            keep_count = int(population_size * 0.2)
            population = population[:keep_count]
            
            # Add new diverse solutions
            diverse_solutions = get_diverse_initial_solutions(adj_list, num_solutions=5)
            for solution_dict in diverse_solutions:
                chromosome = [solution_dict.get(i, 1) for i in range(num_vertices)]
                unique_colors = list(set(chromosome))
                color_map = {old_color: (i % num_colors) + 1 for i, old_color in enumerate(unique_colors)}
                chromosome = [color_map[color] for color in chromosome]
                population.append(chromosome)
            
            # Fill rest randomly
            while len(population) < population_size:
                chromosome = [random.randint(1, num_colors) for _ in range(num_vertices)]
                population.append(chromosome)
            
            stagnation_counter = 0

        # --- 7. Elite Preservation ---
        new_population = []
        elite_count = int(population_size * 0.15)
        new_population.extend([ind[:] for ind in population[:elite_count]])

        # --- 8. Advanced Reproduction ---
        while len(new_population) < population_size:
            # Tournament selection
            parent1 = min(random.sample(list(zip(population, fitness_scores)), tournament_size), 
                         key=lambda x: x[1])[0]
            parent2 = min(random.sample(list(zip(population, fitness_scores)), tournament_size), 
                         key=lambda x: x[1])[0]

            if random.random() < crossover_rate:
                child = conflict_aware_crossover(parent1, parent2, adj_list)
            else:
                child = parent1[:]

            # Mutation
            for i in range(num_vertices):
                if random.random() < current_mutation_rate:
                    child[i] = random.randint(1, num_colors)
            
            new_population.append(child)
        
        population = new_population[:population_size]
    
    if verbose:
        print("\nAdvanced MA run finished.")
        if best_fitness_overall == 0:
            final_colors = len(set(best_solution_overall))
            print(f"Found a valid solution with {final_colors} colors.")
        else:
            print(f"Could not find a valid solution. Best attempt had {best_fitness_overall} conflicts.")

    return best_solution_overall 

def run_multistart_enhanced_algorithm(adj_list, num_vertices, num_colors, num_runs=3, verbose=True):
    """
    Run the advanced algorithm multiple times with different starting conditions
    and return the best solution found.
    """
    if verbose:
        print(f"\n🚀 MULTISTART ADVANCED ALGORITHM - {num_runs} independent runs")
        print("=" * 70)
    
    best_overall_solution = None
    best_overall_fitness = float('inf')
    best_run_number = 0
    
    for run in range(num_runs):
        if verbose:
            print(f"\n⚡ Starting Run #{run + 1}/{num_runs}")
            print("-" * 50)
        
        # Set different random seed for each run
        random.seed(42 + run * 1000)
        
        # Run the advanced algorithm
        solution = run_enhanced_memetic_algorithm(adj_list, num_vertices, num_colors, verbose=verbose)
        
        if solution:
            fitness = calculate_fitness(solution, adj_list)
            
            if fitness < best_overall_fitness:
                best_overall_fitness = fitness
                best_overall_solution = solution[:]
                best_run_number = run + 1
                
                if verbose:
                    print(f"🏆 NEW BEST SOLUTION found in Run #{run + 1}!")
                    print(f"   Fitness: {best_overall_fitness}")
                    if fitness == 0:
                        colors_used = len(set(solution))
                        print(f"   Valid coloring with {colors_used} colors!")
            
            if verbose:
                print(f"Run #{run + 1} completed. Fitness: {fitness}")
        else:
            if verbose:
                print(f"Run #{run + 1} failed to produce a solution.")
    
    if verbose:
        print(f"\n🎯 MULTISTART RESULTS SUMMARY:")
        print(f"   Best solution found in Run #{best_run_number}")
        print(f"   Best fitness achieved: {best_overall_fitness}")
        if best_overall_fitness == 0:
            final_colors = len(set(best_overall_solution))
            print(f"   ✅ VALID COLORING with {final_colors} colors!")
        else:
            print(f"   ❌ No valid coloring found. Best attempt had {best_overall_fitness} conflicts.")
    
    return best_overall_solution 
