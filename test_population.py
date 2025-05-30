# test_population.py

from src.init_population import initialize_population

# 5 birey, 100 şehir
pop = initialize_population(5, 100)
for i, ind in enumerate(pop):
    print(f"Individual {i+1}:", ind)
