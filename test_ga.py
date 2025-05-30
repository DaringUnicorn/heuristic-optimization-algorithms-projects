# test_ga.py

from src.parse_tsp import load_custom_tsp, compute_dist_matrix
from src.ga_tsp import run_ga

coords = load_custom_tsp("instances/tsp_100_1")
D = compute_dist_matrix(coords)

best, length = run_ga(
    D,
    pop_size=25,
    generations=50,
    tourn_size=5,
    p_crossover=0.8,
    p_mutation=0.1,
    elite_size=2
)

print("Best tour length:", length)
print("Best tour:", best)
