from typing import List, Optional
from pyeda.inter import BinaryDecisionDiagram
from .PetriNet import PetriNet
import numpy as np
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, value, PULP_CBC_CMD # new lib

def deadlock_reachable_marking(pn: PetriNet, bdd: BinaryDecisionDiagram) -> Optional[List[int]]:
    """
    Tìm marking deadlock khả dĩ trong Petri Net `pn` thỏa mãn ràng buộc BDD `bdd`.
    Sử dụng ILP để kiểm tra deadlock cho mỗi marking.
    """
    all_places = pn.place_ids # all_places = danh sách tên các places, ví dụ ['p1','p2','p3'].
                              # Ta cần đánh giá token ở tất cả places để xem deadlock xảy ra hay không.

    for sol in bdd.satisfy_all(): #trả về tất cả nghiệm thỏa ràng buộc BDD.
        # Biến đã có giá trị
        var_map = {str(k): int(v) for k, v in sol.items()}
        constrained = set(var_map.keys()) # các place đã được ràng buộc trong BDD.
        unconstrained = [p for p in all_places if p not in constrained] # các place chưa được ràng buộc trong BDD.
        # tránh thiếu do satisful_all() chỉ sinh các biến xuất hiện trong BDD.

        # Sinh tất cả giá trị cho các place chưa constrain
        n_unconstrained = len(unconstrained)
        for i in range(2 ** n_unconstrained):
            marking = []
            for p in all_places:
                if p in constrained:
                    marking.append(var_map[p])
                else:
                    idx = unconstrained.index(p)
                    marking.append((i >> idx) & 1)

            if _is_deadlock_ilp(pn, marking):
                return marking  # Trả về deadlock đầu tiên tìm được

    return None  # Không có deadlock

def _is_deadlock_ilp(pn: PetriNet, marking: List[int]) -> bool:
    """
    Kiểm tra deadlock bằng ILP:
    - Biến t[i] nhị phân: transition i có thể enable không
    - Maximize sum(t)
    - Nếu max sum(t) == 0 → deadlock
    """
    n_trans = len(pn.trans_ids)
    n_places = len(pn.place_ids)
    m = np.array(marking) # vector marking hiện tại (token ở từng place)

    # Tạo bài toán ILP
    prob = LpProblem("DeadlockCheck", LpMaximize)   #Tạo 1 bài toán tối ưu tên "DeadlockCheck"
                                                    #LpMaximize nghĩa là bài toán dạng maximize (tối đa hóa).
    t = [LpVariable(f"t{i}", cat='Binary') for i in range(n_trans)]

    # Mục tiêu: maximize số transition có thể enable
    prob += lpSum(t)

    # Ràng buộc cho từng transition
    for i in range(n_trans):
        for j in range(n_places):
            # transition i cần token ở place j
            if pn.I[i][j] == 1:
                prob += t[i] <= m[j]
            # safe constraint: firing transition không vượt quá 1 token
            if m[j] - pn.I[i][j] + pn.O[i][j] > 1:
                prob += t[i] == 0

    # Giải ILP
    prob.solve(PULP_CBC_CMD(msg=0))

    # Nếu max sum(t) == 0 → không có transition enable → deadlock
    return value(prob.objective) == 0
