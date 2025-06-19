# test_ga.py
# Simple sanity check for GA fitness and solution quality

from parser import read_graph
from ga_coloring import ga_coloring, fitness
import time

# 1) Load graph
G = read_graph("gc_50_9.txt")

# 2) Run GA with lighter settings for speed
start = time.time()
best = ga_coloring(
    G,
    pop_size=100,
    generations=100,
    crossover_rate=0.8,
    mutation_rate=0.1,
    elitism_rate=0.1,
    sa_temp=1.0,
    sa_cooling=0.95,
    sa_steps=1,        # only 1 SA step for quick test
    tournament_k=3
)
dur = time.time() - start

# 3) Evaluate fitness and verify
raw_score = fitness(best, G)
conflicts = sum(
    1
    for u, nbrs in G.items()
    for v in nbrs
    if best[u] == best[v]
) // 2
colors_used = len(set(best))

# 4) Print results
print(f"Raw fitness: {raw_score}")
print(f"  -> conflicts: {conflicts}")
print(f"  -> colors used: {colors_used}")
print(f"Runtime: {dur:.2f}s")
