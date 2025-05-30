from src.parse_tsp import load_custom_tsp, compute_dist_matrix
from src.fitness import fitness


# 1) Instance with 100 cities
coords = load_custom_tsp("instances/tsp_100_1")
print("Number of cities:", len(coords))

# 2) Distance matrix
D = compute_dist_matrix(coords)
print("Distance matrix shape:", len(D), "x", len(D[0]))

# 3) Example tour
tour = list(range(len(coords)))
length = fitness(tour, D)
print("Tour length:", length)

