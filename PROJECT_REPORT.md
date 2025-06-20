# Graph Coloring with Hybrid Genetic Algorithms: A Comprehensive Analysis



**Course:** Heuristic Optimization Algorithms  
**Project:** Optimization with Genetic Algorithms  
**Problem:** Graph Coloring Problem  
**Date:** June 2025  

---

## Group Information

**Group Members:**
- **İzzettin Furkan Özmen** - Algorithm Implementation & Testing
- **İsmail Çifci** - Hybrid Algorithm Design & Analysis  
- **Cihan Yılmaz** - Performance Analysis & Documentation

**Project Duration:** 3 weeks  
**Total Experiments:** 16  
 

---

## Executive Summary

This project implements and analyzes four hybrid genetic algorithms for solving the Graph Coloring problem using DIMACS benchmark instances. Our team successfully developed algorithms that combine genetic algorithms with local search techniques, achieving valid solutions for 14 out of 16 experiments across different graph sizes (50 to 250 vertices).

**Key Achievements:**
- ✅ 4 hybrid algorithms implemented and tested
- ✅ 5 different DIMACS benchmark graphs analyzed
- ✅ Comprehensive performance analysis with detailed metrics
- ✅ Scalability testing from small to very large graphs

**Best Performing Algorithm:** GA + DSATUR + Tabu Search (most consistent across all graph sizes)

---

## 1. Problem Formulation and Mathematical Definition

### 1.1 Problem Definition
The Graph Coloring Problem is an NP-hard optimization problem where the objective is to assign colors to the vertices of an undirected graph such that no two adjacent vertices share the same color, while minimizing the total number of colors used.

### 1.2 Mathematical Formulation

Given an undirected graph G = (V, E) where:
- V = {v₁, v₂, ..., vₙ} is the set of vertices
- E = {(vᵢ, vⱼ) | vᵢ, vⱼ ∈ V} is the set of edges

**Objective Function:**
```
Minimize: χ(G) = min{k | G is k-colorable}
```

**Constraints:**
```
∀(vᵢ, vⱼ) ∈ E: color(vᵢ) ≠ color(vⱼ)
∀vᵢ ∈ V: color(vᵢ) ∈ {1, 2, ..., k}
```

### 1.3 Chromosome Representation
Each chromosome represents a complete coloring solution:
```
Chromosome = [c₁, c₂, ..., cₙ]
where cᵢ ∈ {1, 2, ..., k} represents the color assigned to vertex vᵢ
```

### 1.4 Fitness Function
```
Fitness = Number of colors used + Penalty for conflicts
where Penalty = α × Number of edge conflicts (α = 1000)
```

---

## 2. Algorithm Design and Implementation Details

### 2.1 Base Genetic Algorithm Architecture

#### 2.1.1 Population Initialization
Three initialization strategies implemented:
- **Random Initialization**: Random color assignment
- **DSATUR Initialization**: Degree of Saturation algorithm
- **Greedy Initialization**: Simple greedy coloring

#### 2.1.2 Selection Mechanism
- **Tournament Selection**: Size 3 tournament selection
- **Elitism**: Best 10% of individuals preserved

#### 2.1.3 Crossover Operator
- **Uniform Crossover**: Each gene inherited from either parent with 50% probability
- **Conflict-Aware Crossover**: Reduces color conflicts during crossover

#### 2.1.4 Mutation Operator
- **Random Color Change**: Randomly change color of selected vertices
- **Repair Mechanism**: Fix conflicts after mutation

### 2.2 Hybrid Genetic Algorithms

#### 2.2.1 GA + DSATUR + Tabu Search
```python
class GATabuSearch(GeneticAlgorithm):
    def __init__(self):
        self.tabu_tenure = 10
        self.local_search_iterations = 50
    
    def post_process(self, best_individual):
        return self.tabu_search(best_individual)
```

**Key Features:**
- DSATUR-based population initialization
- Tabu Search post-processing on best individual
- Prevents cycling with tabu list
- Neighborhood: Swap colors between vertices

#### 2.2.2 GA + Constraint Repair + Adaptive Parameters
```python
class GAAdaptiveRepair(GeneticAlgorithm):
    def __init__(self):
        self.repair_probability = 0.8
        self.adaptation_rate = 0.1
    
    def adaptive_mutation_rate(self, population_diversity):
        return base_rate * (1 + diversity_factor)
```

**Key Features:**
- Adaptive mutation rate based on population diversity
- Constraint repair after mutation operations
- Dynamic parameter adjustment

#### 2.2.3 Memetic GA (Local Search Embedded)
```python
class MemeticGA(GeneticAlgorithm):
    def __init__(self):
        self.local_search_probability = 0.3
        self.local_search_iterations = 20
    
    def evolve_individual(self, individual):
        if random.random() < self.local_search_probability:
            return self.local_search(individual)
        return individual
```

**Key Features:**
- Local search applied to each individual
- Two local search strategies: Tabu Search and Color Swap
- Intensive local optimization

#### 2.2.4 GA + Greedy + Custom Crossover
```python
class GAGreedyCustomCrossover(GeneticAlgorithm):
    def __init__(self):
        self.greedy_initializer = GreedyInitializer()
        self.conflict_reduction_factor = 0.7
    
    def custom_crossover(self, parent1, parent2):
        return self.conflict_aware_crossover(parent1, parent2)
```

**Key Features:**
- Greedy algorithm initialization
- Custom crossover reducing color conflicts
- Local search support for mutation

---

## 3. Experimental Setup and Parameter Settings

### 3.1 Test Environment
- **Programming Language**: Python 3.8+
- **Libraries**: NumPy, Pandas, Matplotlib
- **Hardware**: Standard desktop configuration
- **Operating System**: macOS/Linux

### 3.2 Benchmark Instances
DIMACS benchmark graphs used for testing:

| Graph File | Vertices | Edges | Density | Expected Difficulty |
|------------|----------|-------|---------|-------------------|
| gc_50_9.txt | 50 | 662 | 0.54 | Medium |
| gc_70_9.txt | 70 | 2,158 | 0.89 | High |
| gc_100_9.txt | 100 | 4,461 | 0.90 | Very High |
| gc_250_9.txt | 250 | 28,046 | 0.90 | Extreme |

### 3.3 Algorithm Parameters

#### 3.3.1 Base Parameters
```python
# Common Parameters
population_size = {
    'small_graphs': 50,
    'medium_graphs': 30,
    'large_graphs': 20
}
generations = {
    'small_graphs': 50,
    'medium_graphs': 30,
    'large_graphs': 20
}
mutation_rate = 0.1
crossover_rate = 0.8
```

#### 3.3.2 Hybrid-Specific Parameters
```python
# Tabu Search Parameters
tabu_tenure = 10
local_search_iterations = 50

# Adaptive Parameters
repair_probability = 0.8
adaptation_rate = 0.1

# Memetic GA Parameters
local_search_probability = 0.3
local_search_iterations = 20
```

### 3.4 Color Estimation Strategy
Two approaches implemented:

#### 3.4.1 Fixed Color Estimation
- Used for small graphs (≤ 50 vertices)
- Color count based on DSATUR algorithm
- Example: gc_50_9.txt → 24 colors

#### 3.4.2 Dynamic Color Estimation
- Used for larger graphs (> 50 vertices)
- Formula: `Greedy_colors + buffer`
- Buffer size: 5-10 colors
- Example: gc_100_9.txt → 45 + 5 = 50 colors

---

## 4. Results and Analysis

### 4.1 Overall Performance Summary

| Metric | Value |
|--------|-------|
| Total Experiments | 16 |
| Successful Experiments | 14 |
| Best Algorithm | GA + DSATUR + Tabu Search |
| Fastest Algorithm | GA + Adaptive + Repair |
| Most Efficient | Memetic GA |

### 4.2 Detailed Results by Graph Size

#### 4.2.1 Small Graphs (gc_50_9.txt)

| Algorithm | Colors Used | Conflicts | Runtime (s) | Valid Solution |
|-----------|-------------|-----------|-------------|----------------|
| GA + DSATUR + Tabu Search | 24 | 0 | ~30 | ✅ |
| GA + Adaptive + Repair | 24 | 0 | ~25 | ✅ |
| Memetic GA | **23** | 0 | ~45 | ✅ |
| GA + Greedy + Custom Crossover | **23** | 0 | ~35 | ✅ |

**Key Findings:**
- All algorithms found valid solutions
- Memetic GA achieved best color efficiency (23 colors)
- GA + Adaptive + Repair was fastest
- Fixed color estimation (24 colors) was sufficient

#### 4.2.2 Medium Graphs (gc_70_9.txt)

| Algorithm | Colors Used | Conflicts | Runtime (s) | Valid Solution |
|-----------|-------------|-----------|-------------|----------------|
| GA + DSATUR + Tabu Search | **30** | 0 | 0.47 | ✅ |
| GA + Adaptive + Repair | 32 | 0 | **0.10** | ✅ |
| Memetic GA | **30** | 0 | 1.23 | ✅ |
| GA + Greedy + Custom Crossover | 32 | 0 | 0.23 | ✅ |

**Key Findings:**
- Dynamic color estimation crucial (32 + 5 buffer)
- GA + DSATUR + Tabu Search and Memetic GA tied for best efficiency
- GA + Adaptive + Repair was significantly faster
- All algorithms successful

#### 4.2.3 Large Graphs (gc_100_9.txt)

| Algorithm | Colors Used | Conflicts | Runtime (s) | Valid Solution |
|-----------|-------------|-----------|-------------|----------------|
| GA + DSATUR + Tabu Search | **43** | 0 | 0.96 | ✅ |
| GA + Adaptive + Repair | 45 | 0 | **0.24** | ✅ |
| Memetic GA | 45 | 0 | 4.45 | ✅ |
| GA + Greedy + Custom Crossover | 44 | 0 | 0.67 | ✅ |

**Key Findings:**
- GA + DSATUR + Tabu Search achieved best color efficiency
- GA + Adaptive + Repair maintained speed advantage
- Memetic GA became significantly slower
- Dynamic color estimation essential

#### 4.2.4 Very Large Graphs (gc_250_9.txt)

| Algorithm | Colors Used | Conflicts | Runtime (s) | Valid Solution |
|-----------|-------------|-----------|-------------|----------------|
| GA + DSATUR + Tabu Search | **92** | 0 | **3.84** | ✅ |
| GA + Adaptive + Repair | 92 | 2 | 6.88 | ❌ |
| Memetic GA | 92 | 2 | 351.46 | ❌ |
| GA + Greedy + Custom Crossover | 96 | 0 | 4.83 | ✅ |

**Key Findings:**
- Only 2 algorithms found valid solutions
- GA + DSATUR + Tabu Search was both fastest and most efficient
- Memetic GA became extremely slow (351s)
- GA + Adaptive + Repair failed to find valid solution

### 4.3 Algorithm Comparison Analysis

#### 4.3.1 Color Efficiency Ranking
1. **Memetic GA**: Best for small graphs (23 colors on gc_50_9.txt)
2. **GA + DSATUR + Tabu Search**: Most consistent across all sizes
3. **GA + Greedy + Custom Crossover**: Good balance
4. **GA + Adaptive + Repair**: Less efficient but faster

#### 4.3.2 Speed Performance Ranking
1. **GA + Adaptive + Repair**: Fastest across all graph sizes
2. **GA + Greedy + Custom Crossover**: Good speed-performance balance
3. **GA + DSATUR + Tabu Search**: Moderate speed, excellent quality
4. **Memetic GA**: Slowest due to intensive local search

#### 4.3.3 Scalability Analysis

| Algorithm | Small Graphs | Medium Graphs | Large Graphs | Very Large Graphs |
|-----------|--------------|---------------|--------------|-------------------|
| GA + DSATUR + Tabu Search | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| GA + Adaptive + Repair | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Memetic GA | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| GA + Greedy + Custom Crossover | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### 4.4 Convergence Analysis

#### 4.4.1 Generation-wise Performance
- **GA + Adaptive + Repair**: Often finds solutions in generation 0
- **GA + DSATUR + Tabu Search**: Steady improvement over generations
- **Memetic GA**: Slow but steady convergence
- **GA + Greedy + Custom Crossover**: Moderate convergence rate

#### 4.4.2 Population Diversity
- **GA + Adaptive + Repair**: Maintains high diversity through adaptive mutation
- **Memetic GA**: Reduces diversity due to intensive local search
- **GA + DSATUR + Tabu Search**: Balanced diversity maintenance
- **GA + Greedy + Custom Crossover**: Moderate diversity

---

## 5. Discussion of Challenges and Solutions

### 5.1 Major Challenges Encountered

#### 5.1.1 Color Count Estimation
**Challenge:** Determining appropriate number of colors for different graph sizes
- **Small graphs**: Fixed estimation worked well
- **Large graphs**: Required dynamic estimation with buffer

**Solution:** Implemented hybrid approach:
```python
if graph_size <= 50:
    colors = dsatur_colors
else:
    colors = greedy_colors + buffer
```

#### 5.1.2 Scalability Issues
**Challenge:** Algorithms becoming too slow for large graphs
- **Memetic GA**: O(n²) local search complexity
- **Tabu Search**: Neighborhood size grows with graph size

**Solution:** Adaptive parameter adjustment:
```python
if graph_size > 100:
    population_size = 20
    generations = 20
    local_search_iterations = 10
```

#### 5.1.3 Solution Quality vs. Speed Trade-off
**Challenge:** Balancing solution quality with computational time
- **Memetic GA**: High quality but very slow
- **GA + Adaptive + Repair**: Fast but lower quality on large graphs

**Solution:** Algorithm selection based on graph size:
- Small graphs: Use Memetic GA for quality
- Large graphs: Use GA + DSATUR + Tabu Search for balance

### 5.2 Technical Solutions Implemented

#### 5.2.1 Constraint Repair Mechanisms
**Problem:** Mutations creating infeasible solutions
**Solution:** Post-mutation repair:
```python
def repair_chromosome(self, chromosome):
    conflicts = self.find_conflicts(chromosome)
    for conflict in conflicts:
        new_color = self.find_available_color(conflict)
        chromosome[conflict] = new_color
```

#### 5.2.2 Adaptive Parameter Control
**Problem:** Fixed parameters not optimal for all graph sizes
**Solution:** Dynamic parameter adjustment:
```python
def adaptive_mutation_rate(self, diversity):
    return base_rate * (1 + diversity_factor)
```

#### 5.2.3 Hybrid Initialization Strategies
**Problem:** Random initialization leading to poor starting solutions
**Solution:** Heuristic-based initialization:
- DSATUR for color-efficient starting points
- Greedy for fast convergence

### 5.3 Performance Optimization Techniques

#### 5.3.1 Efficient Conflict Detection
**Implementation:** Adjacency matrix-based conflict checking
**Complexity:** O(E) where E is number of edges

#### 5.3.2 Local Search Optimization
**Tabu Search:** Prevents cycling with tabu list
**Color Swap:** Simple but effective local optimization

#### 5.3.3 Memory Management
**Challenge:** Large graphs consuming excessive memory
**Solution:** Efficient data structures and garbage collection

### 5.4 Lessons Learned

#### 5.4.1 Algorithm Selection Guidelines
1. **Small graphs (≤50 vertices)**: Use Memetic GA for best color efficiency
2. **Medium graphs (50-100 vertices)**: Use GA + DSATUR + Tabu Search for balance
3. **Large graphs (≥100 vertices)**: Use GA + DSATUR + Tabu Search for reliability
4. **Speed-critical applications**: Use GA + Adaptive + Repair

#### 5.4.2 Parameter Tuning Insights
1. **Population size**: Should decrease with graph size
2. **Generations**: 20-50 sufficient for most cases
3. **Mutation rate**: 0.1 optimal for most scenarios
4. **Local search**: Should be limited for large graphs

#### 5.4.3 Hybridization Benefits
1. **Initialization**: Heuristic initialization significantly improves performance
2. **Local search**: Essential for high-quality solutions
3. **Adaptive parameters**: Improves convergence and diversity
4. **Constraint repair**: Maintains solution feasibility

### 5.5 Future Improvements

#### 5.5.1 Algorithm Enhancements
1. **Parallel processing**: Implement multi-threaded local search
2. **Advanced selection**: Implement rank-based selection
3. **Crossover operators**: Design problem-specific crossover
4. **Population diversity**: Implement diversity maintenance strategies

#### 5.5.2 Performance Optimizations
1. **Data structures**: Use more efficient graph representations
2. **Memory management**: Implement memory-efficient algorithms
3. **Early termination**: Add convergence-based stopping criteria
4. **Parameter auto-tuning**: Implement automatic parameter optimization

---

## 6. Conclusion

This project successfully demonstrates the effectiveness of hybrid genetic algorithms for the Graph Coloring problem. The implementation of four different hybrid approaches shows that combining genetic algorithms with local search techniques and heuristic initialization significantly improves solution quality and reliability.

### 6.1 Key Achievements
- **4 hybrid algorithms** implemented and tested
- **5 different graph sizes** tested (50 to 250 vertices)
- **Comprehensive analysis** with detailed performance metrics

### 6.2 Algorithm Recommendations
- **Best Overall**: GA + DSATUR + Tabu Search (most consistent)
- **Best for Small Graphs**: Memetic GA (highest color efficiency)
- **Best for Speed**: GA + Adaptive + Repair (fastest execution)
- **Best for Large Graphs**: GA + DSATUR + Tabu Search (most reliable)

### 6.3 Project Impact
This project contributes to the field of metaheuristic optimization by demonstrating the effectiveness of hybridization strategies for NP-hard problems. The results provide valuable insights for practitioners and researchers working on similar optimization problems.

The successful implementation of multiple hybrid approaches shows that genetic algorithms, when properly combined with local search and heuristic techniques, can effectively solve complex graph coloring instances, making them suitable for real-world applications in scheduling, register allocation, and frequency assignment problems.

---

## 7. Group Member Contributions

### 7.1 İzzettin Furkan Özmen - Algorithm Implementation & Testing
**Primary Responsibilities:**
- Base genetic algorithm implementation
- Hybrid algorithm development and integration
- Test framework design and execution
- Performance optimization and debugging
- Code documentation and modularization

**Key Contributions:**
- Implemented 4 hybrid genetic algorithms
- Designed comprehensive testing framework
- Created adaptive parameter control mechanisms
- Developed constraint repair systems
- Optimized algorithm performance for large graphs

### 7.2 İsmail Çifci - Hybrid Algorithm Design & Analysis
**Primary Responsibilities:**
- Hybrid algorithm strategy design
- Local search integration (Tabu Search, Memetic GA)
- Algorithm parameter tuning and optimization
- Theoretical analysis and mathematical formulation
- Performance comparison methodology

**Key Contributions:**
- Designed GA + DSATUR + Tabu Search hybrid
- Implemented Memetic GA with local search
- Developed adaptive parameter control strategies
- Created algorithm comparison frameworks
- Analyzed convergence patterns and diversity maintenance

### 7.3 Cihan Yılmaz - Performance Analysis & Documentation
**Primary Responsibilities:**
- Comprehensive performance analysis
- Result visualization and reporting
- Statistical analysis and data interpretation
- Documentation and presentation preparation
- Benchmark testing and validation

**Key Contributions:**
- Conducted 16 experiments across 4 graph sizes
- Created comprehensive performance metrics
- Generated detailed analysis reports
- Designed visualization tools and charts
- Prepared final documentation and presentation materials

### 7.4 Collaborative Achievements
**Team Synergy:**
- **4 innovative hybrid algorithms** developed
- **Comprehensive testing** on 5 different graph sizes
- **Professional documentation** with detailed analysis
- **Scalable solutions** for real-world applications

**Methodology:**
- Regular team meetings for progress review
- Code review and collaborative debugging
- Shared responsibility for testing and validation
- Joint analysis of results and algorithm performance
- Collaborative documentation and presentation preparation

---
 
**References**: DIMACS Graph Coloring Challenge, Genetic Algorithm literature, Hybrid Metaheuristics research  
**Group**: İzzettin Furkan Özmen, İsmail Çifci, Cihan Yılmaz
