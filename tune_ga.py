# tune_ga.py
# Grid‐search parameter tuning for GA

from parser import read_graph
from ga_coloring import tune_parameters

# Load graph
G = read_graph("gc_50_9.txt")

# Define parameter grid
param_grid = {
    'pop_size':      [50, 100, 200],
    'generations':   [100, 200],
    'mutation_rate': [0.01, 0.05, 0.1],
    'crossover_rate':[0.7, 0.9],
    'elitism_rate':  [0.1, 0.2],
    'sa_steps':      [1, 5, 10]
}

# Run tuning
best_params = tune_parameters(G, param_grid)
print("Best parameters found:", best_params)
