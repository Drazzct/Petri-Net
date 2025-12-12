import numpy as np
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from pyeda.inter import *

def test_001():
    P = ["p1", "p2", "p3"]
    T = ["t1", "t2", "t3"]
    I = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    O = np.array([[0,1,0],
                  [0,0,1],
                  [1,0,0]])
    M0 = np.array([1,0,0])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, ~p2, p3),
                    And(~p1, p2, ~p3),
                    And(p1, ~p2, ~p3))

    assert count == 3
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_002():
    P = ["p1", "p2", "p3"]
    T = ["t1", "t2", "t3"]
    I = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    O = np.array([[0,1,0],
                  [0,0,1],
                  [1,0,0]])
    M0 = np.array([1,0,1])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, p2, p3),
                    And(p1, p2, ~p3),
                    And(p1, ~p2, p3))

    assert count == 3
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_003():
    P = ["p1", "p2", "p3"]
    T = ["t1", "t2", "t3"]
    I = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    O = np.array([[0,1,0],
                  [0,0,1],
                  [1,0,0]])
    M0 = np.array([1,1,1])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(p1, p2, p3))

    assert count == 1
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_004():
    P = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'] # 7
    T = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']
    I = np.array([[1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0]])
    O = np.array([[0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0]])
    M0 = np.array([1, 0, 0, 0, 0, 0, 0])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3, p4, p5, p6, p7 = [exprvar(i) for i in P]
    expected_expr = Or(
        And(~p1, ~p2, ~p3, ~p4, ~p5, ~p6, p7),
        And(~p1, ~p2, ~p3, p4, ~p5, p6, ~p7),
        And(~p1, ~p2, ~p3, p4, p5, ~p6, ~p7),
        And(~p1, ~p2, p3, ~p4, ~p5, p6, ~p7),
        And(~p1, ~p2, p3, ~p4, p5, ~p6, ~p7),
        And(~p1, p2, ~p3, ~p4, ~p5, p6, ~p7),
        And(~p1, p2, ~p3, ~p4, p5, ~p6, ~p7),
        And(p1, ~p2, ~p3, ~p4, ~p5, ~p6, ~p7)
    )
    
    assert count == 8
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_005():
    P = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']
    T = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']
    I = np.array([[1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0]])
    O = np.array([[0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0]])
    M0 = np.array([1, 0, 0, 0, 0, 1, 0])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3, p4, p5, p6, p7 = [exprvar(i) for i in P]
    expected_expr = Or(
        And(~p1, ~p2, ~p3, ~p4, ~p5, p6, p7),
        And(~p1, ~p2, ~p3, ~p4, p5, ~p6, p7),
        And(~p1, ~p2, ~p3, p4, p5, p6, ~p7),
        And(~p1, ~p2, p3, ~p4, p5, p6, ~p7),
        And(~p1, p2, ~p3, ~p4, p5, p6, ~p7),
        And(p1, ~p2, ~p3, ~p4, ~p5, p6, ~p7)
    )
        
    assert count == 6
    assert bdd2expr(bdd).equivalent(expected_expr) 

def test_007():
    P = ['P1', 'P2', 'P3', 'P4', 'P5']
    T = ['T1', 'T2', 'T3', 'T4']
    I = np.array([
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0]
    ])
    O = np.array([
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1]
    ])
    M0 = np.array([1, 0, 0, 0, 0])
    bdd, count = bdd_reachable(PetriNet(P, T, P, T, I, O, M0))

    p1, p2, p3, p4, p5 = [exprvar(i) for i in P]
    expected_expr = Or(
        And(~p1, p2, ~p3, p4, p5),
        And(~p1, p2, p3, p4, ~p5),
        And(p1, ~p2, ~p3, ~p4, ~p5),
        And(p1, ~p2, ~p3, p4, p5),
        And(p1, ~p2, p3, p4, ~p5),
        And(p1, p2, ~p3, ~p4, ~p5)
    )

    assert count == 6
    assert bdd2expr(bdd).equivalent(expected_expr) 