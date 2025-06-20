from collections import deque
from base_genetic_algorithm import GeneticAlgorithm
import random

class TabuSearch:
    """
    A simple Tabu Search implementation for graph coloring.
    It attempts to improve a given coloring by changing the colors of conflicting vertices.
    """
    def __init__(self, graph, initial_coloring, max_iterations=1000, tabu_tenure=10):
        self.graph = graph
        self.current_solution = list(initial_coloring)
        self.best_solution = list(initial_coloring)
        self.max_iterations = max_iterations
        self.tabu_list = deque(maxlen=tabu_tenure)
        self.num_colors = len(set(initial_coloring))

    def _calculate_conflicts(self, coloring):
        conflicts = 0
        conflicting_vertices = set()
        for v, neighbors in self.graph.adj.items():
            for u in neighbors:
                if v < u and coloring[v] == coloring[u]:
                    conflicts += 1
                    conflicting_vertices.add(v)
                    conflicting_vertices.add(u)
        return conflicts, list(conflicting_vertices)

    def run(self):
        best_conflicts = self._calculate_conflicts(self.best_solution)[0]

        for i in range(self.max_iterations):
            current_conflicts, conflicting_vertices = self._calculate_conflicts(self.current_solution)

            if current_conflicts < best_conflicts:
                self.best_solution = list(self.current_solution)
                best_conflicts = current_conflicts
                print(f"  Tabu Search new best: {best_conflicts} conflicts")

            if best_conflicts == 0:
                print("  Tabu Search found a valid solution!")
                break

            if not conflicting_vertices:
                # No conflicts, we are done
                break

            best_move = None
            best_move_conflicts = float('inf')

            # Explore neighborhood of a random conflicting vertex
            vertex_to_move = random.choice(conflicting_vertices)
            
            for color in range(self.num_colors):
                if color == self.current_solution[vertex_to_move]:
                    continue

                original_color = self.current_solution[vertex_to_move]
                
                # Aspiration criterion: allow tabu move if it leads to a new best solution
                is_tabu = (vertex_to_move, color) in self.tabu_list
                
                self.current_solution[vertex_to_move] = color
                new_conflicts, _ = self._calculate_conflicts(self.current_solution)

                if is_tabu and new_conflicts >= best_conflicts:
                     # Revert move and continue
                    self.current_solution[vertex_to_move] = original_color
                    continue

                if new_conflicts < best_move_conflicts:
                    best_move_conflicts = new_conflicts
                    best_move = (vertex_to_move, color, original_color)
                
                # Revert move
                self.current_solution[vertex_to_move] = original_color

            if best_move:
                vertex, new_color, old_color = best_move
                self.current_solution[vertex] = new_color
                # Add the reverse move to the tabu list
                self.tabu_list.append((vertex, old_color))
        
        return self.best_solution, best_conflicts


class ColorSwap:
    """
    A simple Color Swap local search for graph coloring.
    Swaps colors between vertices to reduce conflicts.
    """
    def __init__(self, graph, max_iterations=100):
        self.graph = graph
        self.max_iterations = max_iterations

    def _calculate_conflicts(self, coloring):
        conflicts = 0
        for v, neighbors in self.graph.adj.items():
            for u in neighbors:
                if v < u and coloring[v] == coloring[u]:
                    conflicts += 1
        return conflicts

    def run(self, chromosome):
        """
        Apply color swap local search to improve the chromosome.
        """
        improved = list(chromosome)
        current_conflicts = self._calculate_conflicts(improved)
        
        for iteration in range(self.max_iterations):
            if current_conflicts == 0:
                break
                
            # Find a random conflict
            conflicting_pairs = []
            for v, neighbors in self.graph.adj.items():
                for u in neighbors:
                    if v < u and improved[v] == improved[u]:
                        conflicting_pairs.append((v, u))
            
            if not conflicting_pairs:
                break
                
            # Pick a random conflict
            v1, v2 = random.choice(conflicting_pairs)
            
            # Try swapping colors
            original_v1, original_v2 = improved[v1], improved[v2]
            improved[v1], improved[v2] = improved[v2], improved[v1]
            
            new_conflicts = self._calculate_conflicts(improved)
            
            # Keep the swap only if it improves the solution
            if new_conflicts < current_conflicts:
                current_conflicts = new_conflicts
            else:
                # Revert the swap
                improved[v1], improved[v2] = original_v1, original_v2
        
        return improved, current_conflicts


class ConstraintRepair:
    """
    Repairs constraint violations in chromosomes by changing colors of conflicting vertices.
    """
    def __init__(self, graph, max_repair_attempts=10):
        self.graph = graph
        self.max_repair_attempts = max_repair_attempts

    def _find_conflicts(self, chromosome):
        """Find all conflicting vertex pairs."""
        conflicts = []
        for v, neighbors in self.graph.adj.items():
            for u in neighbors:
                if v < u and chromosome[v] == chromosome[u]:
                    conflicts.append((v, u))
        return conflicts

    def repair(self, chromosome, num_colors):
        """
        Attempts to repair constraint violations in the chromosome.
        Returns the repaired chromosome and number of conflicts remaining.
        """
        repaired = list(chromosome)
        attempts = 0
        
        while attempts < self.max_repair_attempts:
            conflicts = self._find_conflicts(repaired)
            
            if not conflicts:
                break  # No conflicts, chromosome is valid
                
            # Pick a random conflict and try to fix it
            v1, v2 = random.choice(conflicts)
            
            # Try to change the color of v1 to resolve the conflict
            original_color = repaired[v1]
            
            # Find available colors for v1
            neighbor_colors = set()
            for neighbor in self.graph.adj[v1]:
                neighbor_colors.add(repaired[neighbor])
            
            # Try to find a color that doesn't conflict with neighbors
            for color in range(num_colors):
                if color not in neighbor_colors and color != original_color:
                    repaired[v1] = color
                    break
            else:
                # If no good color found, pick a random one
                available_colors = [c for c in range(num_colors) if c != original_color]
                if available_colors:
                    repaired[v1] = random.choice(available_colors)
            
            attempts += 1
        
        final_conflicts = len(self._find_conflicts(repaired))
        return repaired, final_conflicts


class GreedyInitializer:
    """
    Greedy initialization for genetic algorithm population.
    Uses a simple greedy coloring approach.
    """
    def __init__(self, graph):
        self.graph = graph

    def greedy_coloring(self):
        """
        Simple greedy coloring algorithm.
        """
        coloring = {}
        used_colors = set()
        
        # Sort vertices by degree (highest first)
        vertices = sorted(self.graph.adj.keys(), 
                         key=lambda v: len(self.graph.adj[v]), reverse=True)
        
        for vertex in vertices:
            # Find the smallest available color
            neighbor_colors = set()
            for neighbor in self.graph.adj[vertex]:
                if neighbor in coloring:
                    neighbor_colors.add(coloring[neighbor])
            
            # Find the smallest color not used by neighbors
            color = 0
            while color in neighbor_colors:
                color += 1
            
            coloring[vertex] = color
            used_colors.add(color)
        
        # Convert to list format
        result = [0] * len(self.graph.adj)
        for vertex, color in coloring.items():
            result[vertex] = color
        
        return result, len(used_colors)


class CustomCrossover:
    """
    Custom crossover operator that reduces color conflicts.
    """
    def __init__(self, graph):
        self.graph = graph

    def _calculate_conflicts(self, chromosome):
        """Calculate number of conflicts in a chromosome."""
        conflicts = 0
        for v, neighbors in self.graph.adj.items():
            for u in neighbors:
                if v < u and chromosome[v] == chromosome[u]:
                    conflicts += 1
        return conflicts

    def crossover(self, parent1, parent2):
        """
        Custom crossover that tries to reduce conflicts.
        Uses conflict-aware uniform crossover.
        """
        child1 = list(parent1)
        child2 = list(parent2)
        
        # For each position, choose the color that causes fewer conflicts
        for i in range(len(parent1)):
            # Test both colors at this position
            temp1 = child1.copy()
            temp2 = child2.copy()
            
            # Swap colors at position i
            temp1[i] = parent2[i]
            temp2[i] = parent1[i]
            
            # Calculate conflicts for both options
            conflicts1 = self._calculate_conflicts(temp1)
            conflicts2 = self._calculate_conflicts(temp2)
            
            # Choose the better option
            if conflicts1 < conflicts2:
                child1[i] = parent2[i]
            else:
                child2[i] = parent1[i]
        
        return child1, child2


class MemeticGA(GeneticAlgorithm):
    """
    Memetic Genetic Algorithm with Local Search Embedded.
    Each individual undergoes local search (Tabu Search or Color Swap) after genetic operations.
    """
    def __init__(self, graph, population_size, num_colors, 
                 local_search_type="tabu", local_search_iterations=50):
        super().__init__(graph, population_size, num_colors, initializer='mixed')
        self.local_search_type = local_search_type
        self.local_search_iterations = local_search_iterations
        self.tabu_search = TabuSearch(graph, [], max_iterations=local_search_iterations)
        self.color_swap = ColorSwap(graph, max_iterations=local_search_iterations)
        print(f"🚀 Using Memetic GA: GA + {local_search_type.title()} Local Search")

    def _apply_local_search(self, chromosome):
        """
        Apply local search to improve a single chromosome.
        """
        if self.local_search_type == "tabu":
            # For Tabu Search, we need to create a new instance with the current chromosome
            tabu = TabuSearch(
                self.graph, 
                chromosome, 
                max_iterations=self.local_search_iterations
            )
            improved, conflicts = tabu.run()
            return improved
        elif self.local_search_type == "color_swap":
            improved, conflicts = self.color_swap.run(chromosome)
            return improved
        else:
            return chromosome

    def _run_generation(self):
        """
        Override the generation method to include local search for each individual.
        """
        # Calculate fitness for all individuals
        fitness_scores = [(chromo, self._calculate_fitness(chromo)) for chromo in self.population]
        
        # Sort by fitness (lower is better)
        fitness_scores.sort(key=lambda x: x[1][0])
        
        # Get the best individual (for elitism)
        best_chromosome = fitness_scores[0][0]
        
        # Create new population
        new_population = [best_chromosome[:]]  # Elitism
        
        # Generate the rest of the population
        while len(new_population) < self.population_size:
            parent1 = self._selection()
            parent2 = self._selection()
            offspring1, offspring2 = self._crossover(parent1, parent2)
            offspring1 = self._mutation(offspring1)
            offspring2 = self._mutation(offspring2)
            
            # Apply local search to improve offspring
            offspring1 = self._apply_local_search(offspring1)
            offspring2 = self._apply_local_search(offspring2)
            
            new_population.append(offspring1)
            if len(new_population) < self.population_size:
                new_population.append(offspring2)
                
        return new_population


class GAAdaptiveRepair(GeneticAlgorithm):
    """
    Hybrid GA with Constraint Repair and Adaptive Parameters.
    - Repairs chromosomes after mutation
    - Adjusts mutation rate based on population diversity
    """
    def __init__(self, graph, population_size, num_colors, 
                 base_mutation_rate=0.1, diversity_threshold=0.3):
        super().__init__(graph, population_size, num_colors, initializer='mixed')
        self.base_mutation_rate = base_mutation_rate
        self.diversity_threshold = diversity_threshold
        self.constraint_repair = ConstraintRepair(graph)
        print("🚀 Using Hybrid Algorithm: GA + Constraint Repair + Adaptive Parameters")

    def _calculate_population_diversity(self):
        """
        Calculate population diversity based on average Hamming distance.
        """
        if len(self.population) < 2:
            return 0.0
        
        total_distance = 0
        comparisons = 0
        
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                distance = sum(1 for a, b in zip(self.population[i], self.population[j]) if a != b)
                total_distance += distance
                comparisons += 1
        
        if comparisons == 0:
            return 0.0
            
        avg_distance = total_distance / comparisons
        max_possible_distance = len(self.population[0])
        diversity = avg_distance / max_possible_distance
        
        return diversity

    def _adaptive_mutation_rate(self):
        """
        Adjust mutation rate based on population diversity.
        - Low diversity -> higher mutation rate
        - High diversity -> lower mutation rate
        """
        diversity = self._calculate_population_diversity()
        
        if diversity < self.diversity_threshold:
            # Low diversity, increase mutation rate
            adaptive_rate = min(0.5, self.base_mutation_rate * 2.0)
        else:
            # High diversity, decrease mutation rate
            adaptive_rate = max(0.01, self.base_mutation_rate * 0.5)
        
        return adaptive_rate

    def _mutation_with_repair(self, chromosome):
        """
        Apply mutation and then repair constraints.
        """
        # Get adaptive mutation rate
        mutation_rate = self._adaptive_mutation_rate()
        
        # Apply mutation
        mutated = list(chromosome)
        for i in range(len(mutated)):
            if random.random() < mutation_rate:
                mutated[i] = random.randint(0, self.num_colors - 1)
        
        # Repair constraints
        repaired, conflicts = self.constraint_repair.repair(mutated, self.num_colors)
        
        return repaired

    def _run_generation(self):
        """
        Override the generation method to use adaptive mutation with repair.
        """
        # Calculate fitness for all individuals
        fitness_scores = [(chromo, self._calculate_fitness(chromo)) for chromo in self.population]
        
        # Sort by fitness (lower is better)
        fitness_scores.sort(key=lambda x: x[1][0])
        
        # Get the best individual (for elitism)
        best_chromosome = fitness_scores[0][0]
        
        # Create new population
        new_population = [best_chromosome[:]]  # Elitism
        
        # Generate the rest of the population
        while len(new_population) < self.population_size:
            parent1 = self._selection()
            parent2 = self._selection()
            offspring1, offspring2 = self._crossover(parent1, parent2)
            
            # Use adaptive mutation with repair
            offspring1 = self._mutation_with_repair(offspring1)
            offspring2 = self._mutation_with_repair(offspring2)
            
            new_population.append(offspring1)
            if len(new_population) < self.population_size:
                new_population.append(offspring2)
                
        return new_population


class GAGreedyCustomCrossover(GeneticAlgorithm):
    """
    Hybrid GA with Greedy Initialization and Custom Crossover.
    - Uses Greedy algorithm for initialization
    - Custom crossover that reduces color conflicts
    - Local search supported mutation
    """
    def __init__(self, graph, population_size, num_colors, 
                 local_search_iterations=30):
        # Override initialization to use greedy
        self.graph = graph
        self.population_size = population_size
        self.num_colors = num_colors
        
        # Initialize components
        self.greedy_initializer = GreedyInitializer(graph)
        self.custom_crossover = CustomCrossover(graph)
        self.color_swap = ColorSwap(graph, max_iterations=local_search_iterations)
        
        # Initialize population with greedy algorithm
        self._initialize_population()
        
        print("🚀 Using Hybrid Algorithm: GA + Greedy + Custom Crossover")

    def _initialize_population(self):
        """
        Initialize population using greedy algorithm and some random individuals.
        """
        self.population = []
        
        # Add greedy solution
        greedy_solution, greedy_colors = self.greedy_initializer.greedy_coloring()
        self.population.append(greedy_solution)
        
        # Add some variations of greedy solution
        for _ in range(min(5, self.population_size // 2)):
            variation = list(greedy_solution)
            # Randomly change some colors
            for i in range(len(variation)):
                if random.random() < 0.1:  # 10% chance to change
                    variation[i] = random.randint(0, self.num_colors - 1)
            self.population.append(variation)
        
        # Fill the rest with random individuals
        while len(self.population) < self.population_size:
            individual = [random.randint(0, self.num_colors - 1) for _ in range(len(self.graph.adj))]
            self.population.append(individual)

    def _custom_crossover(self, parent1, parent2):
        """
        Use custom crossover that reduces conflicts.
        """
        return self.custom_crossover.crossover(parent1, parent2)

    def _mutation_with_local_search(self, chromosome):
        """
        Apply mutation and then improve with local search.
        """
        # Apply standard mutation
        mutated = list(chromosome)
        for i in range(len(mutated)):
            if random.random() < 0.1:  # 10% mutation rate
                mutated[i] = random.randint(0, self.num_colors - 1)
        
        # Apply local search to improve
        improved, conflicts = self.color_swap.run(mutated)
        
        return improved

    def _run_generation(self):
        """
        Override the generation method to use custom crossover and local search.
        """
        # Calculate fitness for all individuals
        fitness_scores = [(chromo, self._calculate_fitness(chromo)) for chromo in self.population]
        
        # Sort by fitness (lower is better)
        fitness_scores.sort(key=lambda x: x[1][0])
        
        # Get the best individual (for elitism)
        best_chromosome = fitness_scores[0][0]
        
        # Create new population
        new_population = [best_chromosome[:]]  # Elitism
        
        # Generate the rest of the population
        while len(new_population) < self.population_size:
            parent1 = self._selection()
            parent2 = self._selection()
            
            # Use custom crossover
            offspring1, offspring2 = self._custom_crossover(parent1, parent2)
            
            # Use mutation with local search
            offspring1 = self._mutation_with_local_search(offspring1)
            offspring2 = self._mutation_with_local_search(offspring2)
            
            new_population.append(offspring1)
            if len(new_population) < self.population_size:
                new_population.append(offspring2)
                
        return new_population


class GATabuSearch(GeneticAlgorithm):
    """
    Hybrid GA that uses DSATUR for initialization and Tabu Search to
    improve the best individual at the end of the run.
    """
    def __init__(self, graph, population_size, num_colors, tabu_iterations=100, tabu_tenure=10):
        # This approach always initializes with DSATUR
        super().__init__(graph, population_size, num_colors, initializer='dsatur')
        self.tabu_iterations = tabu_iterations
        self.tabu_tenure = tabu_tenure
        print("🚀 Using Hybrid Algorithm: GA + DSATUR + Tabu Search")

    def run(self, generations=100):
        # 1. Run standard GA with DSATUR initialization
        super().run(generations)

        # 2. Improve the best individual with Tabu Search
        print("\n--- Starting Tabu Search post-processing ---")
        best_ga_solution = self.best_chromosome
        initial_conflicts = self.best_conflicts
        
        print(f"Best GA solution has {initial_conflicts} conflicts. Applying Tabu Search...")

        if initial_conflicts == 0:
            print("GA already found a valid solution. No need for Tabu Search.")
            return self.best_chromosome, self.best_fitness, self.best_conflicts, self.best_colors_used

        tabu_search = TabuSearch(
            graph=self.graph,
            initial_coloring=best_ga_solution,
            max_iterations=self.tabu_iterations,
            tabu_tenure=self.tabu_tenure
        )
        
        ts_solution, ts_conflicts = tabu_search.run()

        print(f"Tabu Search finished. Final conflicts: {ts_conflicts}")

        if ts_conflicts < self.best_conflicts:
            print("🎉 Tabu Search found a better solution!")
            self.best_chromosome = ts_solution
            self.best_conflicts = ts_conflicts
            self.best_colors_used = len(set(ts_solution))
            # Recalculate fitness
            self.best_fitness, _ = self._calculate_fitness(ts_solution)
        else:
            print("Tabu Search did not improve the GA solution.")

        return self.best_chromosome, self.best_fitness, self.best_conflicts, self.best_colors_used 
