# src/init_population.py

import random

def initialize_population(pop_size, n_cities):
    """
    Returns a list of pop_size individuals,
    each is a random permutation of 0..n_cities-1
    """
    return [random.sample(range(n_cities), n_cities) for _ in range(pop_size)]
