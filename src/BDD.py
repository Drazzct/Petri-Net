import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from .PetriNet import PetriNet
from collections import deque
import numpy as np

def bdd_reachable(pn: PetriNet,) -> Tuple[BinaryDecisionDiagram, int]:
    max_iterations: int = 10000 # biến này để đảm bảo sẽ ko bị loop vô hạn
    I = pn.I # copy từ PetriNet sang I
    O = pn.O # copy sang O
    
    # Xác định format dựa vào số places thực tế
    n_places = len(pn.place_ids) # P = ["p1", "p2", "p3"] : List 
    # P = ["p1", "p2", "p3"] : List có thể hiểu là array lun, chỉ có list mới xài len() để lấy số elements đc 
    # còn nparray ( tức numpy array ) thì là ma trận chứ k phải mảng, k xài len đc

    # Nếu số cột = số places → format (transitions, places) → cần transpose
    # Nếu số hàng = số places → format (places, transitions) → giữ nguyên
    
    #công thức shape : ví dụ có ma trận A : row,col = [2,3] thì A.shape[0] = 2 , A.shape[1] = 3 . Shape[0] : hàng , shape[1] : cột
    # Format chuẩn theo Petri Net : Hàng = places && Cột = transitions . Tức I phải có form row , col = places , transitions

    if I.shape[1] == n_places and I.shape[0] != n_places: # cột I == place và hàng I != place
        # Format: (transitions, places) → transpose thành (places, transitions)
        I = I.T
        O = O.T
        n_trans = I.shape[1]  # Số transitions = số cột sau khi transpose
    elif I.shape[0] == n_places: # hàng == place 
        # Format: (places, transitions) → giữ nguyên
        n_trans = I.shape[1]
    else:
        raise ValueError(f"Không thể xác định format của ma trận shape {I.shape} với {n_places} places")

    cur_vars = [bddvar(pid) for pid in pn.place_ids]
    next_vars = [bddvar(pid + "_n") for pid in pn.place_ids]

    def marking_to_bdd(mk_tuple):
        result = expr2bdd(expr(True))
        for val, var in zip(mk_tuple, cur_vars): # Ghép từng phần tử của mk_tuple và cur_vars lại thành cặp. 
            # ví dụ có : mk_tuple = (1, 0, 1) và cur_vars = [p0, p1, p2] Thì zip → lần lượt tạo ra:
            #(val=1, var=p0) và (val=0, var=p1) và (val=1, var=p2) → Mỗi vòng lặp xử lý 1 place.
            if val == 1:
                result = result & var
            else:
                result = result & (~var)
        return result

    M0 = tuple(pn.M0.tolist()) # cần chuyển M0 thành tuple vì M0 đang là list (array) mà list là mutable 
    Reach = marking_to_bdd(M0) # chuyển từ marking sang BDD

    trans_relations = [] # lưu từ R1 -> Rn ( == số transtions ) . Với Rx là (p1 & p1_n) & ... tới hết với p1->pN là ở current transitions còn p1_n->pN_n là next transition ( có thể hiểu là cùng 1 transitions , khác ử input và output) 

    for t in range(n_trans):
        rel = expr2bdd(expr(True))# cứ 1 rel sẽ chứa các biến như sau : p1 p1_n p2 p2_n p3 p3_n... ( với p1 p2 p3 ... là input tại 1 transitions nhất định (t1..tN) và p1_n p2_n p3_n ... là output)
        for p in range(n_places):
            cur_var = cur_vars[p] # Lấy ra đúng p1->pN trong cùng 1 transitions
            next_var = next_vars[p] # lấy ra đúng p1_n -> pN_n trong cùng 1 transitions
            inp = int(I[p, t]) # curent value
            out = int(O[p, t]) # output value

            if inp == 0 and out == 0:
                rel = rel & ((next_var & cur_var) | (~next_var & ~cur_var))  # lưu thành ~p1 và ~p1_n ( vẫn == 0)
            elif inp == 1 and out == 0:
                rel = rel & cur_var & (~next_var) # lưu thành p1 và ~p1_n ( biến từ 1 -> 0)
            elif inp == 0 and out == 1:
                rel = rel & (~cur_var) & next_var # lưu thành ~p1 và p1_n ( biến từ 0 -> 1)
            elif inp == 1 and out == 1:
                rel = rel & cur_var & next_var # lưu thành p1 và p1_n ( vẫn == 1 )
        
        trans_relations.append(rel)

    compose_map = {next_vars[i]: cur_vars[i] for i in range(n_places)} # khi gọi .compose thì next sẽ trả về current ( loại bỏ đi _n để đưa vào Reach cho đúng )

    iteration = 0
    while True:
        iteration += 1
        Post_next = expr2bdd(expr(False))

        for trans_rel in trans_relations:
            pairs = Reach & trans_rel # lọc ra tất cả các BDD hiện có trong Reach và thoã mãn đc trans_rel 
            for v in cur_vars:
                pairs = pairs.smoothing(v) # loại bỏ all cur_val , lúc này trong pairs chỉ còn next_val . Lúc này dưới dạng boolean là stage tiếp theo nhưng vẫn dứoi dạng p1_n...
            Post_next = Post_next | pairs 

        Post = Post_next.compose(compose_map) # thay p1_n ... p2_n thành p1...p2
        NewReach = Reach | Post # lấy Or của Post ( marking tìm đc ) với Reach ( all marking hiện tại )

        if NewReach.equivalent(Reach) or iteration >= max_iterations: # check xem nếu ko thêm đc thì break 
            # Ở đây equivalent là hàm so sánh trong peyda xem NewReach và Reach có cùng biểu diễn 1 logic hay ko ?
            Reach = NewReach
            break
        
        Reach = NewReach

    try:
        count = int(Reach.satisfy_count())
    except:
        count = sum(1 for _ in Reach.satisfy_all())

    return Reach, count
