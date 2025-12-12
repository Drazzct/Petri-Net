import collections
from typing import Tuple, List, Optional, Dict, Any
from pyeda.inter import *
from collections import deque
import numpy as np


def max_reachable_marking(
    place_ids: List[str], 
    bdd: BinaryDecisionDiagram, 
    c: np.ndarray
) -> Tuple[Optional[List[int]], Optional[int]]:
    if c is None or len(c) != len(place_ids):
        raise ValueError("c must be an array with same length as place_ids")

    best_marking = None
    best_value = float('-inf')

    try:
        sat_iter = bdd.satisfy_all()
    except Exception as e:
        raise RuntimeError(f"BDD object does not support satisfy_all(): {e}")

    found_any = False
    place_to_idx = {pid: i for i, pid in enumerate(place_ids)}
    
    for assn in sat_iter:
        assign_map = {}
        for var_obj, value in assn.items():
            name = getattr(var_obj, "name", None)
            if name is None:
                name = str(var_obj)
            assign_map[name] = 1 if bool(value) else 0

        marking = [0] * len(place_ids)
        for pid, idx in place_to_idx.items():
            if pid in assign_map:
                marking[idx] = assign_map[pid]
            else:
                marking[idx] = 1 if c[idx] > 0 else 0

        try:
            obj_value = int(np.dot(c, np.array(marking, dtype=int)))
        except Exception:
            obj_value = int(sum(int(marking[i]) * int(c[i]) for i in range(len(c))))

        if obj_value > best_value:
            best_value = obj_value
            best_marking = marking
            found_any = True

    if not found_any:
        return None, None

    return best_marking, best_value
