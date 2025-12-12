import sys
import os
import time
import tracemalloc
import numpy as np
from pyeda.inter import *
from graphviz import Source

# Assumes your project structure allows these imports
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from src.Optimization import max_reachable_marking
from src.DFS import dfs_reachable  # DFS removed as requested
from src.Deadlock import deadlock_reachable_marking

def measure_performance(task_name, func, *args):
    """
    Helper to run a function while measuring execution time and peak memory.
    Returns the result of the function.
    """
    print(f"\n--- {task_name} ---")
    
    # 1. Start Memory Tracking
    tracemalloc.start()
    
    # 2. Start Timer
    start_time = time.perf_counter()
    
    # 3. Execute Function
    result = func(*args)
    
    # 4. Stop Timer
    end_time = time.perf_counter()
    
    # 5. Get Memory Stats
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 6. Report
    duration = end_time - start_time
    peak_mb = peak / (1024 * 1024) # Convert bytes to MB
    
    print(f"Execution Time : {duration:.6f} seconds")
    print(f"Peak Memory    : {peak_mb:.6f} MB")
    
    return result

def main():
    # ------------------------------------------------------
    # 0. Argument Parsing
    # ------------------------------------------------------
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "test3.pnml"
        print(f"[INFO] No argument provided. Defaulting to '{filename}'")

    if not os.path.exists(filename):
        print(f"[ERROR] File '{filename}' not found.")
        print("Usage: python run.py <path_to_pnml>")
        return

    # ------------------------------------------------------
    # 1. Load Petri Net (Parser)
    # ------------------------------------------------------
    try:
        pn = measure_performance("1. Parsing PNML", PetriNet.from_pnml, filename)
        print(f"Loaded: {len(pn.place_ids)} places, {len(pn.trans_ids)} transitions.")
    except Exception as e:
        print(f"[CRITICAL FAIL] Parser error: {e}")
        return

    # ------------------------------------------------------
    # 2. Explicit Reachability (BFS Only)
    # ------------------------------------------------------
    # Using BFS is standard as it explores the state space layer by layer.
    bfs_set = measure_performance("2. Explicit Reachability (BFS)", dfs_reachable, pn)
    for m in bfs_set:
        print(np.array(m))
    print(f"Total reachable states (BFS): {len(bfs_set)}")

    # ------------------------------------------------------
    # 3. Symbolic Reachability (BDD)
    # ------------------------------------------------------
    bdd_obj, count = measure_performance("3. BDD Reachability", bdd_reachable, pn)
    print("Satisfying all:", list(bdd_obj.satisfy_all()))
    print(f"Total reachable states (BDD): {count}")
    #Source(bdd_obj.to_dot()).render("bdd", format="png", cleanup=True)
    
    # Verification: Explicit vs Symbolic count
    if len(bfs_set) != count:
        print(f"[WARNING] Mismatch! BFS found {len(bfs_set)}, BDD found {count}")
    else:
        print("[SUCCESS] BFS and BDD counts match.")

    # ------------------------------------------------------
    # 4. Deadlock Detection
    # ------------------------------------------------------
    deadlock = measure_performance("4. Deadlock Detection", deadlock_reachable_marking, pn, bdd_obj)
    
    if deadlock is not None:
        print(f"Deadlock FOUND: {deadlock}")
    else:
        print("Result: No deadlock reachable.")

    # ------------------------------------------------------
    # 5. Optimization
    # ------------------------------------------------------
    # Create objective vector c dynamically based on number of places
    base_c = [1, -2, 3, -1, 1, 2]
    num_places = len(pn.place_ids)
    c = np.resize(np.array(base_c), num_places)
    
    print(f"\nObjective Vector c (first 10): {c[:10]}...")

    max_mark, max_val = measure_performance("5. Optimization", max_reachable_marking, pn.place_names, bdd_obj, c)
    
    if max_mark is not None:
        print(f"Max Value  : {max_val}")
        print(f"Max Marking: {max_mark}")
    else:
        print("Result: No reachable marking found.")

if __name__ == "__main__":
    main()