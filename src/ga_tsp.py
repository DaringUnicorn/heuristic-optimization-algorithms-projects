# src/ga_tsp.py

import random
import math
from src.fitness import fitness
from src.init_population import initialize_population

def two_opt(route, dist):
    """
    Basit 2-opt hill climbing: iyileşme kalmayana dek tüm i<j çifti dener.
    """
    n = len(route)
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                # son eleman ile ilk arasında da 2-opt
                if i == 0 and j == n-1:
                    continue
                # mevcut mesafe
                a, b = route[i], route[i+1]
                c, d = route[j], route[(j+1) % n]
                before = dist[a][b] + dist[c][d]
                after  = dist[a][c] + dist[b][d]
                if after + 1e-9 < before:
                    # inversion
                    route[i+1:j+1] = reversed(route[i+1:j+1])
                    improved = True
        # döngü sonunda tekrar dene
    return route

def pmx_crossover(p1, p2):
    n = len(p1)
    c1 = [None]*n; c2 = [None]*n
    i, j = sorted(random.sample(range(n),2))
    map1 = {}; map2 = {}
    for k in range(i, j+1):
        c1[k] = p2[k]
        c2[k] = p1[k]
        map1[p2[k]] = p1[k]
        map2[p1[k]] = p2[k]
    for k in list(range(0,i))+list(range(j+1,n)):
        gene = p1[k]
        while gene in map1:
            gene = map1[gene]
        c1[k] = gene
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
    """
    p_mutation: başlangıç mutasyon oranı (adaptive inner loop)
    """
    n = len(dist_matrix)
    pop = initialize_population(pop_size, n)
    best_ind, best_fit = None, math.inf

    for g in range(generations):
        # ** Adaptive mutation rate **
        mr = p_mutation * (1 - g/(generations-1))
        
        fits = [fitness(ind, dist_matrix) for ind in pop]
        # elitizm
        paired = sorted(zip(fits, pop), key=lambda x: x[0])
        new_pop = [ind.copy() for _, ind in paired[:elite_size]]

        # yeni popülasyon
        while len(new_pop) < pop_size:
            # tournament
            p1 = min(random.sample(list(zip(pop,fits)), tourn_size), key=lambda x: x[1])[0].copy()
            p2 = min(random.sample(list(zip(pop,fits)), tourn_size), key=lambda x: x[1])[0].copy()
            # crossover
            if random.random() < p_crossover:
                c1, c2 = pmx_crossover(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()
            # mutation + 2-opt local search
            c1 = two_opt(swap_mutation(c1, mr), dist_matrix)
            if len(new_pop) < pop_size:
                c2 = two_opt(swap_mutation(c2, mr), dist_matrix)
            new_pop.append(c1)
            if len(new_pop) < pop_size:
                new_pop.append(c2)

        pop = new_pop
        # en iyiyi güncelle
        gen_best_fit, gen_best_ind = min((fitness(i, dist_matrix), i) for i in pop)
        if gen_best_fit < best_fit:
            best_fit, best_ind = gen_best_fit, gen_best_ind.copy()

    return best_ind, best_fit
