from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from src.Optimization import max_reachable_marking
from src.DFS import dfs_reachable
from src.Deadlock import deadlock_reachable_marking
from pyeda.inter import * 
import numpy as np
## from graphviz import Source

def main():
    # ------------------------------------------------------
    # 1. Load Petri Net từ file PNML
    # ------------------------------------------------------
    filename = "example.pnml"   # đổi file tại đây
    print("Loading PNML:", filename)

    pn = PetriNet.from_pnml(filename)
    print("\n--- Petri Net Loaded ---")
    print(pn)

    # # ------------------------------------------------------
    # # 3. DFS reachable
    # # ------------------------------------------------------
    print("\n--- DFS Reachable Markings ---")
    dfs_set = dfs_reachable(pn)
    # for m in dfs_set:
    #     print(np.array(m))
    print("Total DFS reachable =", len(dfs_set))

    # # ------------------------------------------------------
    # # 4. BDD reachable
    # # ------------------------------------------------------
    print("\n--- BDD Reachable ---")
    bdd, count = bdd_reachable(pn)
    print("--- Satisfying assignments ---")
    for sat in bdd.satisfy_all():
        line = ", ".join(f"{var.names[0]}={val}" for var, val in sat.items())
        print(line)
    print("BDD reachable markings =", count)
    ## Source(bdd.to_dot()).render("bdd", format="png", cleanup=True)

    # # ------------------------------------------------------
    # # 5. Deadlock detection
    # # ------------------------------------------------------
    print("\n--- Deadlock reachable marking ---")
    dead = deadlock_reachable_marking(pn, bdd)
    if dead is not None:
        print("Deadlock marking:", dead)
    else:
        print("No deadlock reachable.")

    # # # ------------------------------------------------------
    # # # 6. Optimization: maximize c·M
    # # # ------------------------------------------------------
    print("\n--- Optimize c·M ---")
    with open("input.txt", "r") as f_in:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            C = np.array(list(map(int, line.split())))
            max_mark, max_val = max_reachable_marking(pn.place_ids, bdd, C)
            print("Max marking:", " ".join(map(str, max_mark)), "Max value:", max_val)


if __name__ == "__main__":
    main()
