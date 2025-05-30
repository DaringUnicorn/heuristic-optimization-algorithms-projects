# src/ga_tsp.py

import random
from src.fitness import fitness
from src.init_population import initialize_population

def tournament_selection(pop, fits, k):
    picks = random.sample(list(zip(pop, fits)), k)
    return min(picks, key=lambda x: x[1])[0].copy()

def pmx_crossover(p1, p2):
    """
    Robust PMX for permutations p1, p2.
    Returns two valid children c1, c2.
    """
    n = len(p1)
    # Child’ları None ile başlat
    c1 = [None] * n
    c2 = [None] * n

    # 1) İki kesme noktası seç
    i, j = sorted(random.sample(range(n), 2))

    # 2) Segmenti takasla ve mapping dict oluştur
    map1 = {}
    map2 = {}
    for k in range(i, j+1):
        c1[k] = p2[k]
        c2[k] = p1[k]
        map1[p2[k]] = p1[k]
        map2[p1[k]] = p2[k]

    # 3) Geriye kalan pozisyonları doldur
    for k in list(range(0, i)) + list(range(j+1, n)):
        # child1 için
        gene = p1[k]
        # eğer gene map1 içinde, mapping zincirini takip et
        while gene in map1:
            gene = map1[gene]
        c1[k] = gene

        # child2 için aynı mantık
        gene = p2[k]
        while gene in map2:
            gene = map2[gene]
        c2[k] = gene

    return c1, c2

def swap_mutation(ind, mr):
    n = len(ind)
    for x in range(n):
        if random.random() < mr:
            y = random.randrange(n)
            ind[x], ind[y] = ind[y], ind[x]
    return ind

def run_ga(dist_matrix,
           pop_size=100,
           generations=200,
           tourn_size=5,
           p_crossover=0.8,
           p_mutation=0.2,
           elite_size=2):
    n = len(dist_matrix)
    pop = initialize_population(pop_size, n)
    best_ind, best_fit = None, float('inf')

    for g in range(generations):
        fits = [fitness(ind, dist_matrix) for ind in pop]
        # elitizm
        paired = sorted(zip(fits, pop), key=lambda x: x[0])
        new_pop = [ind.copy() for _, ind in paired[:elite_size]]

        # geri kalan
        while len(new_pop) < pop_size:
            p1 = tournament_selection(pop, fits, tourn_size)
            p2 = tournament_selection(pop, fits, tourn_size)
            if random.random() < p_crossover:
                c1, c2 = pmx_crossover(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()
            new_pop.append(swap_mutation(c1, p_mutation))
            if len(new_pop) < pop_size:
                new_pop.append(swap_mutation(c2, p_mutation))

        pop = new_pop
        # güncel en iyi
        gen_best_fit, gen_best_ind = min((fitness(i, dist_matrix), i) for i in pop)
        if gen_best_fit < best_fit:
            best_fit, best_ind = gen_best_fit, gen_best_ind.copy()

    return best_ind, best_fit
