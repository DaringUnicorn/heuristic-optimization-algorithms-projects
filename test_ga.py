# test_ga.py

from parser import read_graph
from ga_coloring import ga_coloring, fitness
import time

# 1) Grafı oku
G = read_graph("gc_50_9.txt")

# 2) GA’yı çalıştır ve süreyi ölç
start = time.time()
best = ga_coloring(G)
dur = time.time() - start

# 3) Fitness’i hesapla
raw_score = fitness(best, G)

# 4) Çatışma sayısını kontrol et
conflicts = 0
for u, nbrs in G.items():
    for v in nbrs:
        if best[u] == best[v]:
            conflicts += 1
conflicts //= 2  # kenarlar iki kez sayıldı

# 5) Kullanılan renk sayısı
colors_used = len(set(best))

print(f"Raw fitness: {raw_score}")
print(f"  -> conflicts: {conflicts}")
print(f"  -> colors used: {colors_used}")
print(f"Runtime: {dur:.2f}s")
