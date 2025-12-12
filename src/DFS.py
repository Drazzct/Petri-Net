from collections import deque
import numpy as np
from .PetriNet import PetriNet
from typing import Set, Tuple # new lib

def dfs_reachable(pn: PetriNet) -> Set[Tuple[int, ...]]:  
    I = np.asarray(pn.I, dtype=int)
    O = np.asarray(pn.O, dtype=int)
    M0 = np.asarray(pn.M0, dtype=int).reshape(-1)

    if I.shape != O.shape:
        raise ValueError(f"I and O must have the same shape, got I{I.shape} vs O{O.shape}")

    m = M0.shape[0]  

    # Decide orientation by matching M0 length to the "places" axis
    # Case 1: I is (places, transitions)
    if I.shape[0] == m:
        I_full = I
        O_full = O
    # Case 2: I is (transitions, places) -> transpose to (places, transitions)
    elif I.shape[1] == m:
        I_full = I.T
        O_full = O.T
    else:
        raise ValueError(
            f"Cannot align matrices with M0: len(M0)={m}, I shape={I.shape}."
            f"Expected I to have either rows==len(M0) (P×T) or cols==len(M0) (T×P)."
        )

    n_places, n_trans = I_full.shape

    start = tuple(int(x) for x in M0.tolist())
    visited: Set[Tuple[int, ...]] = set()

    def dfs(marking: Tuple[int, ...]):
        if marking in visited:
            return
        visited.add(marking)

        m_vec = np.array(marking, dtype=int)

        for t in range(n_trans):
            if np.any(m_vec < I_full[:, t]):
                continue
            new_vec = m_vec - I_full[:, t] + O_full[:, t]
            if np.any(new_vec > 1) or np.any(new_vec < 0):
                continue
            dfs(tuple(int(x) for x in new_vec.tolist()))

    dfs(start)
    return visited
