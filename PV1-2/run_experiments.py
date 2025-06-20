import time
import pandas as pd
from parser import read_graph
from backtracking import color_backtrack
from greedy import greedy_coloring, dsatur_coloring

def run_all(graph_files: list[str], k: int, bt_limit: int = 50) -> list[tuple[str, int|None, float|None, int, float, int, float]]:
    """
    Run coloring experiments on multiple graph files.
    Args:
        graph_files: list of file paths (e.g., ["gc_50_9.txt", ...])
        k: max colors for backtracking
        bt_limit: skip backtracking for graphs larger than this
    Returns:
        List of tuples:
        (filename, colors_bt, time_bt, colors_gr, time_gr, colors_ds, time_ds)
        where colors_bt and time_bt are None if graph size > bt_limit
    """
    results = []
    for fp in graph_files:
        print(f"\nProcessing {fp}...")
        G = read_graph(fp)
        n = len(G)
        
        # Run backtracking only if graph is small enough
        if n <= bt_limit:
            print("Running backtracking...")
            start = time.time()
            sol_bt = color_backtrack(G, k)
            t_bt = time.time() - start
            colors_bt = len(set(sol_bt.values())) if sol_bt else 0
        else:
            print(f"Skipping backtracking (graph size {n} > limit {bt_limit})")
            colors_bt = None
            t_bt = None
        
        # Run greedy
        print("Running greedy...")
        start = time.time()
        sol_gr = greedy_coloring(G)
        t_gr = time.time() - start
        colors_gr = len(set(sol_gr.values()))
        
        # Run DSATUR
        print("Running DSATUR...")
        start = time.time()
        sol_ds = dsatur_coloring(G)
        t_ds = time.time() - start
        colors_ds = len(set(sol_ds.values()))
        
        results.append((fp, colors_bt, t_bt, colors_gr, t_gr, colors_ds, t_ds))
        
        # Print results for this file
        print(f"\nResults for {fp}:")
        if colors_bt is not None:
            print(f"Backtracking: {colors_bt} colors, {t_bt:.2f} seconds")
        print(f"Greedy: {colors_gr} colors, {t_gr:.2f} seconds")
        print(f"DSATUR: {colors_ds} colors, {t_ds:.2f} seconds")
    
    return results

if __name__ == "__main__":
    files = ["gc_50_9.txt", "gc_70_9.txt", "gc_100_9.txt", "gc_250_9.txt", "gc_500_9.txt"]
    results = run_all(files, k=9, bt_limit=50)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(results, columns=[
        'filename', 'colors_bt', 'time_bt', 
        'colors_gr', 'time_gr', 
        'colors_ds', 'time_ds'
    ])
    
    # Print formatted results
    print("\nSummary Table:")
    print(df.to_string(index=False))
    
    # Save to CSV
    df.to_csv('results.csv', index=False)
    print("\nResults saved to results.csv")
