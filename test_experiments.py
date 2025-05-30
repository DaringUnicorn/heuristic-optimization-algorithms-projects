# test_experiments.py

import csv
from src.parse_tsp import load_custom_tsp, compute_dist_matrix
from src.ga_tsp import run_ga

# 1) Veri ve mesafe matrisi
coords = load_custom_tsp("instances/tsp_100_1")
D = compute_dist_matrix(coords)

# 2) Parametre aralıkları"
pop_sizes   = [20, 50, 100]
mut_rates   = [0.1, 0.2, 0.3]
gen_counts  = [50, 100]
tourn_size  = 5
p_crossover = 0.8
elite_size  = 2
repeats     = 3  # Her kombinasyondan ortalama almak için

# 3) CSV’yi aç
with open("results/experiments.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["pop_size", "mutation_rate", "generations", "run", "best_length"])

    # 4) Tüm kombinasyonlar
    for pop in pop_sizes:
        for mr in mut_rates:
            for gen in gen_counts:
                for run in range(1, repeats+1):
                    best, length = run_ga(
                        D,
                        pop_size=pop,
                        generations=gen,
                        tourn_size=tourn_size,
                        p_crossover=p_crossover,
                        p_mutation=mr,
                        elite_size=elite_size
                    )
                    writer.writerow([pop, mr, gen, run, length])
                    print(f"Done pop={pop}, mr={mr}, gen={gen}, run={run}, length={length:.2f}")
