import pandas as pd
import matplotlib.pyplot as plt

# 1) CSV’yi oku
df = pd.read_csv('results/experiments.csv')

# 2) Ortalama ve standart sapmayı hesapla
summary = df.groupby(
    ['pop_size','mutation_rate','generations']
)['best_length'].agg(['mean','std']).reset_index()

print(summary)

# 3) Örneğin pop_size ile performans ilişkisini görselleştir
for gen in summary['generations'].unique():
    sub = summary[summary['generations']==gen]
    plt.figure()
    for mr in sub['mutation_rate'].unique():
        data = sub[sub['mutation_rate']==mr]
        plt.plot(data['pop_size'], data['mean'], label=f'mr={mr}')
    plt.title(f'Avg Best Length vs Pop Size (gens={gen})')
    plt.xlabel('Population Size')
    plt.ylabel('Average Best Length')
    plt.legend()
    plt.tight_layout()
    plt.show()
