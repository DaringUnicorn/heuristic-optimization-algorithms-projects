import pandas as pd
import matplotlib.pyplot as plt
import re
import sys

def extract_size(filename: str) -> int:
    """Extract graph size from filename (e.g., 'gc_50_9.txt' -> 50)"""
    match = re.search(r'gc_(\d+)_', filename)
    return int(match.group(1)) if match else 0

def plot(csv_path: str) -> None:
    """
    Reads a CSV with columns:
      filename, colors_bt, time_bt, colors_gr, time_gr, colors_ds, time_ds
    and creates two plots:
      - graph size vs colors_bt, colors_gr, colors_ds
      - graph size vs time_bt, time_gr, time_ds
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Extract graph sizes from filenames
    df['size'] = df['filename'].apply(extract_size)
    df = df.sort_values('size')  # Sort by graph size
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Graph Size vs Colors Used
    ax1.plot(df['size'], df['colors_bt'], 'ro-', label='Backtracking')
    ax1.plot(df['size'], df['colors_gr'], 'bo-', label='Greedy')
    ax1.plot(df['size'], df['colors_ds'], 'go-', label='DSATUR')
    ax1.set_xlabel('Graph Size (number of nodes)')
    ax1.set_ylabel('Number of Colors Used')
    ax1.set_title('Graph Size vs Colors Used')
    ax1.grid(True)
    ax1.legend()
    
    # Plot 2: Graph Size vs Runtime
    ax2.plot(df['size'], df['time_bt'], 'ro-', label='Backtracking')
    ax2.plot(df['size'], df['time_gr'], 'bo-', label='Greedy')
    ax2.plot(df['size'], df['time_ds'], 'go-', label='DSATUR')
    ax2.set_xlabel('Graph Size (number of nodes)')
    ax2.set_ylabel('Runtime (seconds)')
    ax2.set_title('Graph Size vs Runtime')
    ax2.grid(True)
    ax2.legend()
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('coloring_results.png')
    print(f"Plot saved to coloring_results.png")

if __name__ == "__main__":
    # Determine CSV path: use argument or default to results.csv
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'results.csv'
    plot(csv_path)
