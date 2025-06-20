import os
from utils import parse_dimacs_graph
from base_genetic_algorithm import GeneticAlgorithm

def main():
    """
    Main function to load a graph, initialize the GA, and run it.
    """
    # --- Configuration ---
    file_name = "gc_50_9.txt"
    population_size = 100
    num_colors = 9  # Known chromatic number for gc_50_9
    generations = 100 # This will be used later
    initializer = "greedy"  # Options: "random", "dsatur", "greedy", "mixed"
    
    # --- Graph Loading ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "data", file_name)

    try:
        print(f"Loading graph from: {file_path}")
        graph = parse_dimacs_graph(file_path)
        print("Graph loaded successfully!")
        print(graph)
        print("-" * 30)
        print(f"Using initializer: {initializer}")

        # --- GA Initialization and Execution ---
        ga = GeneticAlgorithm(
            graph=graph,
            population_size=population_size,
            num_colors=num_colors,
            initializer=initializer
        )
        
        # The run method currently only prints initial stats
        ga.run(generations=generations)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        print("Please ensure the data file exists and the path is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 
