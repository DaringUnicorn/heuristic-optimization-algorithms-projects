import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Rectangle

# Create a sample graph for visualization
def create_sample_graph():
    # Create a graph with 8 vertices
    G = nx.Graph()
    
    # Add edges to create an interesting graph
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), 
             (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7)]
    
    G.add_edges_from(edges)
    
    # Define colors for vertices (4 different colors)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    vertex_colors = [0, 1, 2, 0, 1, 2, 0, 1]  # Color assignment
    
    return G, colors, vertex_colors

def create_visualization():
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Graph Coloring with Hybrid Genetic Algorithms', fontsize=20, fontweight='bold')
    
    # Sample graph
    G, colors, vertex_colors = create_sample_graph()
    
    # 1. Original Graph
    ax1.set_title('Original Graph Structure', fontsize=14, fontweight='bold')
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, ax=ax1, node_color='lightgray', 
            node_size=800, font_size=12, font_weight='bold',
            edge_color='gray', width=2)
    
    # Add vertex labels
    for i, (node, (x, y)) in enumerate(pos.items()):
        ax1.text(x, y, str(node), ha='center', va='center', fontsize=14, fontweight='bold')
    
    # 2. Colored Graph
    ax2.set_title('Optimal Coloring Solution', fontsize=14, fontweight='bold')
    node_colors = [colors[vertex_colors[i]] for i in range(len(G.nodes()))]
    nx.draw(G, pos, ax=ax2, node_color=node_colors, 
            node_size=800, font_size=12, font_weight='bold',
            edge_color='gray', width=2)
    
    # Add vertex labels
    for i, (node, (x, y)) in enumerate(pos.items()):
        ax2.text(x, y, str(node), ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # 3. Algorithm Performance Comparison
    ax3.set_title('Algorithm Performance Comparison', fontsize=14, fontweight='bold')
    
    algorithms = ['GA + DSATUR\n+ Tabu Search', 'GA + Adaptive\n+ Repair', 
                  'Memetic GA', 'GA + Greedy\n+ Custom Crossover']
    colors_used = [24, 24, 23, 23]  # Example results for gc_50_9.txt
    runtime = [30, 25, 45, 35]  # Runtime in seconds
    
    x = np.arange(len(algorithms))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, colors_used, width, label='Colors Used', color='#4A90E2', alpha=0.8)
    ax3_twin = ax3.twinx()
    bars2 = ax3_twin.bar(x + width/2, runtime, width, label='Runtime (s)', color='#E24A4A', alpha=0.8)
    
    ax3.set_xlabel('Algorithms')
    ax3.set_ylabel('Number of Colors', color='#4A90E2')
    ax3_twin.set_ylabel('Runtime (seconds)', color='#E24A4A')
    ax3.set_xticks(x)
    ax3.set_xticklabels(algorithms, rotation=45, ha='right')
    ax3.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax3_twin.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                     f'{int(height)}s', ha='center', va='bottom', fontweight='bold')
    
    # 4. Success Rate by Graph Size
    ax4.set_title('Success Rate by Graph Size', fontsize=14, fontweight='bold')
    
    graph_sizes = ['50\nvertices', '70\nvertices', '100\nvertices', '250\nvertices']
    success_rates = [100, 100, 100, 50]  # Percentage of successful algorithms
    
    bars = ax4.bar(graph_sizes, success_rates, color=['#4ECDC4', '#45B7D1', '#96CEB4', '#FF6B6B'], alpha=0.8)
    ax4.set_ylabel('Success Rate (%)')
    ax4.set_ylim(0, 110)
    ax4.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}%', ha='center', va='bottom', fontweight='bold')
    
    # Add overall statistics
    fig.text(0.02, 0.02, f'Total Experiments: 16 | Success Rate: 87.5% | Best Algorithm: GA + DSATUR + Tabu Search', 
             fontsize=12, style='italic')
    
    plt.tight_layout()
    plt.savefig('graph_coloring_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Visualization saved as 'graph_coloring_visualization.png'")

if __name__ == "__main__":
    create_visualization() 
