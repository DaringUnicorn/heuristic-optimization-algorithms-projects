import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import math
import time
from heuristics import dsatur_coloring, get_diverse_initial_solutions
from graph_loader import load_graph

class HybridGA:
    def __init__(self, adj_list, num_vertices, num_colors, population_size=150, generations=500, verbose=True):
        self.adj_list = adj_list
        self.num_vertices = num_vertices
        self.num_colors = num_colors
        self.population_size = population_size
        self.generations = generations
        self.verbose = verbose
        # Adaptif parametreler
        self.base_mutation_rate = 0.15
        self.crossover_rate = 0.9
        self.tournament_size = 7
        self.elite_ratio = 0.15
        self.stagnation_limit = 50
        self.temperature = 1.0  # Simulated Annealing için başlangıç sıcaklığı
        self.cooling_rate = 0.995

    def calculate_fitness(self, chromosome):
        conflicts = 0
        for u in self.adj_list:
            for v in self.adj_list[u]:
                if u < v and chromosome[u] == chromosome[v]:
                    conflicts += 1
        # Renk sayısı cezası
        colors_used = len(set(chromosome))
        color_penalty = max(0, colors_used - self.num_colors) * 1000
        return conflicts + color_penalty

    def repair_solution(self, chromosome):
        # Fazla renkleri k aralığına indir
        unique_colors = list(set(chromosome))
        if len(unique_colors) > self.num_colors:
            color_map = {old: ((i % self.num_colors) + 1) for i, old in enumerate(unique_colors)}
            chromosome = [color_map[c] for c in chromosome]
        # Çatışmaları düzelt
        for u in self.adj_list:
            neighbor_colors = {chromosome[v] for v in self.adj_list[u] if v != u}
            if chromosome[u] in neighbor_colors:
                for color in range(1, self.num_colors + 1):
                    if color not in neighbor_colors:
                        chromosome[u] = color
                        break
        return chromosome

    def conflict_aware_crossover(self, parent1, parent2):
        child = [0] * self.num_vertices
        for i in range(self.num_vertices):
            color1 = parent1[i]
            color2 = parent2[i]
            # Daha az çatışma yaratanı seç
            conflicts1 = sum(1 for v in self.adj_list.get(i, []) if parent1[v] == color1)
            conflicts2 = sum(1 for v in self.adj_list.get(i, []) if parent2[v] == color2)
            if conflicts1 < conflicts2:
                child[i] = color1
            elif conflicts2 < conflicts1:
                child[i] = color2
            else:
                child[i] = random.choice([color1, color2])
        return self.repair_solution(child)

    def classic_mutation(self, chromosome, mutation_rate):
        for i in range(self.num_vertices):
            if random.random() < mutation_rate:
                chromosome[i] = random.randint(1, self.num_colors)
        return chromosome

    def swap_mutation(self, chromosome, mutation_rate):
        if random.random() < mutation_rate:
            i, j = random.sample(range(self.num_vertices), 2)
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        return chromosome

    def inversion_mutation(self, chromosome, mutation_rate):
        if random.random() < mutation_rate:
            i, j = sorted(random.sample(range(self.num_vertices), 2))
            chromosome[i:j] = reversed(chromosome[i:j])
        return chromosome

    def simulated_annealing(self, chromosome, fitness):
        # Basit SA: Rastgele bir gen değiştir, kabul olasılığına göre uygula
        i = random.randint(0, self.num_vertices - 1)
        old_color = chromosome[i]
        new_color = random.randint(1, self.num_colors)
        chromosome[i] = new_color
        new_fitness = self.calculate_fitness(chromosome)
        delta = new_fitness - fitness
        if delta < 0 or random.random() < math.exp(-delta / self.temperature):
            return chromosome, new_fitness
        else:
            chromosome[i] = old_color
            return chromosome, fitness

    def run(self, mutation_strategy='classic'):
        # Başlangıç popülasyonu: Sadece 1..k arası renk
        population = []
        diverse_solutions = get_diverse_initial_solutions(self.adj_list, num_solutions=10)
        for sol_dict in diverse_solutions:
            chromo = [((sol_dict.get(i, 1) - 1) % self.num_colors) + 1 for i in range(self.num_vertices)]
            population.append(chromo)
        while len(population) < self.population_size:
            population.append([random.randint(1, self.num_colors) for _ in range(self.num_vertices)])

        best_solution = None
        best_fitness = float('inf')
        stagnation = 0
        mutation_rate = self.base_mutation_rate

        for gen in range(self.generations):
            fitness_scores = [self.calculate_fitness(chromo) for chromo in population]
            sorted_pop = sorted(zip(population, fitness_scores), key=lambda x: x[1])
            population = [item[0] for item in sorted_pop]
            fitness_scores = [item[1] for item in sorted_pop]

            if fitness_scores[0] < best_fitness:
                best_fitness = fitness_scores[0]
                best_solution = population[0][:]
                stagnation = 0
            else:
                stagnation += 1

            # Adaptif mutasyon
            if stagnation > self.stagnation_limit:
                mutation_rate = min(0.5, mutation_rate * 1.5)
                if self.verbose:
                    print(f"[Gen {gen}] Stagnation! Mutation rate increased to {mutation_rate}")
            else:
                mutation_rate = self.base_mutation_rate

            # Elitizm
            elite_count = int(self.population_size * self.elite_ratio)
            new_population = [ind[:] for ind in population[:elite_count]]

            # Hibrit üretim: GA + SA
            while len(new_population) < self.population_size:
                # Gelişmiş turnuva seçimi
                parent1 = min(random.sample(list(zip(population, fitness_scores)), self.tournament_size), key=lambda x: x[1])[0]
                parent2 = min(random.sample(list(zip(population, fitness_scores)), self.tournament_size), key=lambda x: x[1])[0]
                if random.random() < self.crossover_rate:
                    child = self.conflict_aware_crossover(parent1, parent2)
                else:
                    child = parent1[:]
                # Seçilen mutasyon stratejisine göre uygula
                if mutation_strategy == 'classic':
                    child = self.classic_mutation(child, mutation_rate)
                elif mutation_strategy == 'swap':
                    child = self.swap_mutation(child, mutation_rate)
                elif mutation_strategy == 'inversion':
                    child = self.inversion_mutation(child, mutation_rate)
                else:
                    child = self.classic_mutation(child, mutation_rate)
                # Simulated Annealing ile lokal arama
                child, child_fitness = self.simulated_annealing(child, self.calculate_fitness(child))
                new_population.append(child)

            population = new_population[:self.population_size]
            self.temperature *= self.cooling_rate

            # Gerçek zamanlı terminal çıktısı
            if self.verbose and (gen % 10 == 0 or best_fitness == 0):
                print(f"[Gen {gen}] Best fitness: {best_fitness} | Temp: {self.temperature:.4f}")
            if best_fitness == 0:
                print(f"[Gen {gen}] Valid coloring found!")
                break

        return best_solution, best_fitness

# Örnek kullanım:
if __name__ == "__main__":
    num_vertices, num_edges, adj_list = load_graph('gc_50_9.txt')
    for mut in ['classic', 'swap', 'inversion']:
        print(f"\nTesting mutation strategy: {mut}")
        ga = HybridGA(adj_list, num_vertices, num_colors=22, generations=300, verbose=True)
        solution, fitness = ga.run(mutation_strategy=mut)
        print(f"Best solution fitness: {fitness}")
        if fitness == 0:
            print(f"Valid coloring with {len(set(solution))} colors!") 
