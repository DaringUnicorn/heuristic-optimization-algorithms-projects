import random
from initializers import dsatur_initializer, greedy_initializer

class GeneticAlgorithm:
    """
    A Genetic Algorithm to solve the Graph Coloring problem.
    """
    def __init__(self, graph, population_size, num_colors, conflict_penalty=1.0, initializer="random"):
        """
        Initializes the Genetic Algorithm.

        Args:
            graph (Graph): The graph to be colored.
            population_size (int): The number of individuals in the population.
            num_colors (int): The number of available colors (k).
            conflict_penalty (float): The weight for constraint violations (conflicts).
            initializer (str): 'random', 'dsatur', or 'greedy'.
        """
        self.graph = graph
        self.population_size = population_size
        self.num_colors = num_colors
        self.conflict_penalty = conflict_penalty
        self.initializer = initializer
        self.population = self._initialize_population()

    def _initialize_population(self):
        """
        Creates the initial population using the selected initializer.
        """
        population = []
        if self.initializer == "dsatur":
            # First individual: DSATUR
            population.append(dsatur_initializer(self.graph, self.num_colors))
            # The rest: random
            for _ in range(self.population_size - 1):
                chromosome = [random.randint(0, self.num_colors - 1) for _ in range(self.graph.num_vertices)]
                population.append(chromosome)
        elif self.initializer == "greedy":
            # First individual: Greedy
            population.append(greedy_initializer(self.graph, self.num_colors))
            # The rest: random
            for _ in range(self.population_size - 1):
                chromosome = [random.randint(0, self.num_colors - 1) for _ in range(self.graph.num_vertices)]
                population.append(chromosome)
        elif self.initializer == "mixed":
            # 1/3 DSATUR, 1/3 Greedy, 1/3 random
            n_dsatur = self.population_size // 3
            n_greedy = self.population_size // 3
            n_random = self.population_size - n_dsatur - n_greedy
            for _ in range(n_dsatur):
                population.append(dsatur_initializer(self.graph, self.num_colors))
            for _ in range(n_greedy):
                population.append(greedy_initializer(self.graph, self.num_colors))
            for _ in range(n_random):
                chromosome = [random.randint(0, self.num_colors - 1) for _ in range(self.graph.num_vertices)]
                population.append(chromosome)
        else:
            # All random
            for _ in range(self.population_size):
                chromosome = [random.randint(0, self.num_colors - 1) for _ in range(self.graph.num_vertices)]
                population.append(chromosome)
        return population

    def _calculate_fitness(self, chromosome):
        """
        Calculates the fitness of a given chromosome.

        Fitness is defined as: (number of conflicts * penalty) + (number of unique colors).
        A lower fitness score is better.
        """
        conflicts = 0
        # Iterate over each vertex and its neighbors to find conflicts
        for vertex, neighbors in self.graph.adj.items():
            for neighbor in neighbors:
                # To avoid double counting (e.g., edge 1-2 and 2-1), only check one way
                if vertex < neighbor and chromosome[vertex] == chromosome[neighbor]:
                    conflicts += 1
        
        # Calculate the number of unique colors used in the chromosome
        num_unique_colors = len(set(chromosome))
        
        # The penalty ensures that conflict-free solutions are always preferred
        fitness = (conflicts * self.graph.num_vertices) + num_unique_colors
        return fitness, conflicts

    def _selection(self, tournament_size=3):
        """
        Tournament selection to choose parents for reproduction.
        
        Args:
            tournament_size (int): Number of individuals in each tournament.
            
        Returns:
            list: Selected chromosome (parent).
        """
        # Randomly select tournament_size individuals
        tournament = random.sample(self.population, tournament_size)
        
        # Return the best individual from the tournament
        return min(tournament, key=lambda c: self._calculate_fitness(c)[0])

    def _crossover(self, parent1, parent2, crossover_rate=0.8):
        """
        Single-point crossover between two parents.
        
        Args:
            parent1 (list): First parent chromosome.
            parent2 (list): Second parent chromosome.
            crossover_rate (float): Probability of performing crossover.
            
        Returns:
            tuple: Two offspring chromosomes.
        """
        if random.random() > crossover_rate:
            return parent1[:], parent2[:]
        
        # Choose a random crossover point
        crossover_point = random.randint(1, len(parent1) - 1)
        
        # Create offspring by swapping parts
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return offspring1, offspring2

    def _mutation(self, chromosome, mutation_rate=0.1):
        """
        Random mutation of genes in a chromosome.
        
        Args:
            chromosome (list): The chromosome to mutate.
            mutation_rate (float): Probability of mutating each gene.
            
        Returns:
            list: Mutated chromosome.
        """
        mutated = chromosome[:]
        for i in range(len(mutated)):
            if random.random() < mutation_rate:
                # Change to a random color (different from current)
                current_color = mutated[i]
                new_color = random.randint(0, self.num_colors - 1)
                while new_color == current_color and self.num_colors > 1:
                    new_color = random.randint(0, self.num_colors - 1)
                mutated[i] = new_color
        return mutated

    def run(self, generations=100):
        """
        The main loop of the Genetic Algorithm.
        
        Args:
            generations (int): Number of generations to evolve.
        """
        print("Genetic Algorithm started.")
        print(f"Population size: {self.population_size}, Num colors: {self.num_colors}")
        print(f"Generations: {generations}")
        print("-" * 50)

        overall_best_chromosome = None
        overall_best_fitness = float('inf')
        overall_best_conflicts = float('inf')
        overall_best_colors_used = float('inf')

        # Track the best solution found
        best_fitness_history = []
        best_conflicts_history = []
        
        # Main loop
        for generation in range(generations):
            self.population = self._run_generation()
            
            # Find and log the best chromosome of the current generation
            current_best_chromosome, best_fitness_in_gen = min(
                [(chromo, self._calculate_fitness(chromo)[0]) for chromo in self.population], 
                key=lambda x: x[1]
            )
            
            _, best_fitness, best_conflicts, colors_used = self._get_chromosome_details(current_best_chromosome)

            if best_fitness < overall_best_fitness:
                overall_best_chromosome = current_best_chromosome
                overall_best_fitness = best_fitness
                overall_best_conflicts = best_conflicts
                overall_best_colors_used = colors_used

            if (generation + 1) % 10 == 0 or generation == 0:
                print(f"Generation {generation:3d}: Best Fitness = {best_fitness:.2f}, Conflicts = {best_conflicts:2d}, Colors = {colors_used}")

            if overall_best_conflicts == 0:
                print(f"\n🎉 VALID SOLUTION FOUND at generation {generation}!")
                print(f"Colors used: {overall_best_colors_used}\n")
                break
        
        print("\n" + "="*50)
        print("FINAL RESULTS:")
        print(f"Best Fitness: {overall_best_fitness:.2f}")
        print(f"Conflicts: {overall_best_conflicts}")
        print(f"Colors Used: {overall_best_colors_used}")
        if overall_best_conflicts == 0:
            print("✅ VALID SOLUTION ACHIEVED!")
        else:
            print("❌ No valid solution found within the given generations.")

        self.best_chromosome = overall_best_chromosome
        self.best_fitness = overall_best_fitness
        self.best_conflicts = overall_best_conflicts
        self.best_colors_used = overall_best_colors_used

        return overall_best_chromosome, overall_best_fitness, overall_best_conflicts, overall_best_colors_used

    def _run_generation(self):
        """
        Runs a single generation of the genetic algorithm.
        """
        # Calculate fitness for all individuals
        fitness_scores = [(chromo, self._calculate_fitness(chromo)) for chromo in self.population]
        
        # Sort by fitness (lower is better)
        fitness_scores.sort(key=lambda x: x[1][0])
        
        # Get the best individual (for elitism)
        best_chromosome = fitness_scores[0][0]
        
        # Create new population
        new_population = [best_chromosome[:]] # Elitism
        
        # Generate the rest of the population
        while len(new_population) < self.population_size:
            parent1 = self._selection()
            parent2 = self._selection()
            offspring1, offspring2 = self._crossover(parent1, parent2)
            offspring1 = self._mutation(offspring1)
            offspring2 = self._mutation(offspring2)
            new_population.append(offspring1)
            if len(new_population) < self.population_size:
                new_population.append(offspring2)
                
        return new_population

    def _get_chromosome_details(self, chromosome):
        """
        Returns the details of a chromosome.
        """
        fitness, conflicts = self._calculate_fitness(chromosome)
        colors_used = len(set(chromosome))
        return chromosome, fitness, conflicts, colors_used 
