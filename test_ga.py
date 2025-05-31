# test_ga.py

import argparse
from src.parse_tsp import load_custom_tsp, compute_dist_matrix
from src.ga_tsp import run_ga

parser = argparse.ArgumentParser()
parser.add_argument('--pop_size', type=int, default=50)
parser.add_argument('--generations', type=int, default=100)
parser.add_argument('--mutation_rate', type=float, default=0.1)
args = parser.parse_args()

coords = load_custom_tsp("instances/tsp_100_1")
D = compute_dist_matrix(coords)

best, length = run_ga(
    D,
    pop_size=args.pop_size,
    generations=args.generations,
    tourn_size=5,
    p_crossover=0.8,
    p_mutation=args.mutation_rate,
    elite_size=2
)

print("Best tour length:", length)
print("Best tour:", best)
