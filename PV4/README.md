# Graph Coloring with Genetic Algorithms and Hybrid Approaches

This project implements various genetic algorithms and hybrid approaches to solve the Graph Coloring problem using DIMACS benchmark instances. The project demonstrates the effectiveness of combining genetic algorithms with local search techniques and classic heuristics.

## 🎯 Problem Description

The Graph Coloring problem is an NP-hard optimization problem where the goal is to color the vertices of a graph such that no two adjacent vertices have the same color, while minimizing the number of colors used.

## 🏗️ Project Structure

```
PV4/
├── data/                    # DIMACS benchmark graph files
│   ├── gc_50_9.txt         # 50 vertices, 9 colors
│   ├── gc_70_9.txt         # 70 vertices, 9 colors
│   ├── gc_100_9.txt        # 100 vertices, 9 colors
│   ├── gc_250_9.txt        # 250 vertices, 9 colors
│   └── gc_500_9.txt        # 500 vertices, 9 colors
├── results/                 # All result files
├── src/                     # Source code
│   ├── results/            # Temporary result files
│   ├── base_genetic_algorithm.py
│   ├── hybrid_genetic_algorithms.py
│   ├── graph.py
│   ├── initializers.py
│   ├── utils.py
│   ├── main.py
│   ├── experiment_runner.py
│   ├── results_saver.py
│   ├── final_results_saver.py
│   └── test_*.py           # Test files for different graphs
├── README.md               # This file
└── FILE_NAMING_GUIDE.md    # File naming conventions guide
```

## 🧬 Implemented Algorithms

### 1. Base Genetic Algorithm
- **File**: `base_genetic_algorithm.py`
- **Features**: Standard genetic algorithm with tournament selection, uniform crossover, and mutation
- **Parameters**: Population size, generations, mutation rate, crossover rate

### 2. Classic Heuristics
- **DSATUR**: Degree of Saturation algorithm
- **Greedy**: Simple greedy coloring algorithm
- **File**: `test_classic_heuristics.py`

### 3. Hybrid Genetic Algorithms

#### 3.1 GA + DSATUR + Tabu Search
- **File**: `hybrid_genetic_algorithms.py` - `GATabuSearch` class
- **Strategy**: Initialize population with DSATUR, then improve best individual with Tabu Search
- **Advantages**: Good initial solutions, effective local optimization

#### 3.2 GA + Constraint Repair + Adaptive Parameters
- **File**: `hybrid_genetic_algorithms.py` - `GAAdaptiveRepair` class
- **Strategy**: Repair chromosomes after mutation, adapt mutation rate based on population diversity
- **Advantages**: Maintains feasibility, adapts to search progress

#### 3.3 Memetic GA (Local Search Embedded)
- **File**: `hybrid_genetic_algorithms.py` - `MemeticGA` class
- **Strategy**: Each individual undergoes local search (Tabu Search or Color Swap)
- **Advantages**: Strong local optimization, high-quality solutions

#### 3.4 GA + Greedy Initialization + Custom Crossover
- **File**: `hybrid_genetic_algorithms.py` - `GAGreedyCustomCrossover` class
- **Strategy**: Greedy initialization, crossover reduces color conflicts, mutation supported by local search
- **Advantages**: Fast convergence, conflict-aware operations

## 📊 Results Summary

### Performance on Different Graph Sizes

| Graph | Vertices | Best Colors | Best Algorithm |
|-------|----------|-------------|----------------|
| gc_50_9.txt | 50 | 24 | All Hybrids |
| gc_70_9.txt | 70 | 45 | All Hybrids |
| gc_100_9.txt | 100 | 43 | GA + DSATUR + Tabu Search |
| gc_250_9.txt | 250 | 45 | GA + DSATUR + Tabu Search |

### Key Findings
- **Dynamic Color Estimation**: Using Greedy algorithm + buffer for color count estimation significantly improves performance
- **Hybrid Superiority**: All hybrid algorithms outperform base genetic algorithm
- **Scalability**: GA + DSATUR + Tabu Search shows best scalability for larger graphs
- **Solution Quality**: All hybrids find valid conflict-free solutions

## 🚀 Quick Start

### Prerequisites
```bash
pip install numpy pandas matplotlib
```

### Running Tests

1. **Test Classic Heuristics**:
```bash
cd src
python test_classic_heuristics.py
```

2. **Test Hybrid Algorithms on Specific Graph**:
```bash
python test_gc50_graph.py    # Test on gc_50_9.txt
python test_gc100_graph.py   # Test on gc_100_9.txt
python test_gc250_graph.py   # Test on gc_250_9.txt
```

3. **Run All Hybrid Algorithms**:
```bash
python test_hybrid_algorithms.py
```

### Running Experiments
```bash
python experiment_runner.py
```

## 📈 Output Files

### Comprehensive Results
- `results/all_graphs_comprehensive_results.csv` - Complete results for all graphs and algorithms
- `results/comprehensive_analysis_summary.txt` - Detailed analysis in English

### Graph-Specific Results
- `results/hybrid_algorithms_gc50_results.csv` - Results for gc_50_9.txt
- `results/gc100_analysis_report.txt` - Analysis for gc_100_9.txt
- `results/gc250_results_*.csv` - Results for gc_250_9.txt

### Individual Algorithm Results
- `results/classic_heuristics_results.json` - Classic heuristics performance
- `results/genetic_algorithm_results.json` - Base GA performance

## 🔧 Configuration

### Algorithm Parameters
```python
# Base GA Parameters
population_size = 50
generations = 100
mutation_rate = 0.1
crossover_rate = 0.8

# Hybrid GA Parameters
tabu_tenure = 10
local_search_iterations = 50
repair_probability = 0.8
```

### Dynamic Color Estimation
The system automatically estimates the required number of colors using:
```python
estimated_colors = greedy_colors + buffer  # buffer = 5-10 colors
```

## 📝 Key Features

1. **Modular Design**: Easy to add new algorithms or modify existing ones
2. **Comprehensive Testing**: Test files for each graph size
3. **Result Analysis**: Automatic generation of detailed reports
4. **Performance Tracking**: Detailed metrics for each algorithm
5. **Scalability**: Tested on graphs from 50 to 250 vertices

## 🎯 Usage Scenarios

- **Small Graphs (50-70 vertices)**: All hybrid algorithms perform well
- **Medium Graphs (100 vertices)**: GA + DSATUR + Tabu Search recommended
- **Large Graphs (250+ vertices)**: GA + DSATUR + Tabu Search or GA + Greedy + Custom Crossover
- **Research**: Use comprehensive results for algorithm comparison
- **Education**: Study different hybridization strategies

## 🔬 Technical Details

### Graph Representation
- Adjacency matrix representation
- DIMACS format support
- Efficient conflict detection

### Genetic Operators
- **Selection**: Tournament selection
- **Crossover**: Uniform crossover with conflict reduction
- **Mutation**: Random color change with repair mechanisms

### Local Search
- **Tabu Search**: Prevents cycling, improves solution quality
- **Color Swap**: Simple but effective local optimization
- **Constraint Repair**: Maintains solution feasibility

## 📚 References

- DIMACS Graph Coloring Challenge
- Genetic Algorithms for Graph Coloring
- Hybrid Metaheuristics for Combinatorial Optimization
- Tabu Search: A Tutorial

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is for educational and research purposes.

---

**Note**: This project demonstrates the effectiveness of hybrid genetic algorithms for the NP-hard Graph Coloring problem, showing how combining different optimization techniques can lead to better solutions than using any single approach alone. 
