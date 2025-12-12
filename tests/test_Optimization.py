import numpy as np
from src.Optimization import max_reachable_marking
from pyeda.inter import *

def test_001():
    P = ["p1", "p2", "p3"]
    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, ~p2, p3),
                    And(~p1, p2, ~p3),
                    And(p1, ~p2, ~p3))
    bdd = expr2bdd(expected_expr)
    c = np.array([1, 2, 3])

    marking, value = max_reachable_marking(P, bdd, c)
    assert marking == [0,0,1]
    assert value == 3

def test_002():
    P = ["p1", "p2", "p3"]
    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, p2, p3),
                    And(p1, ~p2, p3),
                    And(p1, p2, ~p3))
    bdd = expr2bdd(expected_expr)

    c = np.array([1, -2, 3])
    marking, value = max_reachable_marking(P, bdd, c)
    assert marking == [1,0,1]
    assert value == 4

def test_003():
    P = ["p1", "p2", "p3"]
    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, p2, p3),
                    And(p1, ~p2, p3),
                    And(p1, p2, ~p3))
    bdd = expr2bdd(expected_expr)

    c = np.array([1, -2, -3])
    marking, value = max_reachable_marking(P, bdd, c)
    assert marking == [1,1,0]
    assert value == -1

def test_004():
    P = ["p1", "p2", "p3"]
    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, p2, p3),
                    And(p1, ~p2, p3),
                    And(p1, p2, ~p3),
                    And(p1, p2, p3)
                    )
    bdd = expr2bdd(expected_expr)

    c = np.array([5, 3, -2])
    marking, value = max_reachable_marking(P, bdd, c)
    assert marking == [1,1, 0]
    assert value == 8


def test_005():
    P = ["p1", "p2", "p3"]
    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(And(~p1, p2, p3),
                        And(~p1, p2, ~p3),
                        And(p1, p2, ~p3),
                        And(p1, p2, p3)
                    )
    bdd = expr2bdd(expected_expr)

    c = np.array([1, -2, -2])
    marking, value = max_reachable_marking(P, bdd, c)
    assert marking == [1,1, 0]
    assert value == -1


def test_006():
    P = ["p1", "p2", "p3"]
    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(1, 1)
    bdd = expr2bdd(expected_expr)

    c = np.array([1, -2, -2])
    marking, value = max_reachable_marking(P, bdd, c)
    assert marking == [1, 0, 0]
    assert value == 1

def test_007():
    P = ["p1", "p2", "p3"]
    p1, p2, p3 = exprvar('p1'), exprvar('p2'), exprvar('p3')
    expected_expr = Or(0, 0)
    bdd = expr2bdd(expected_expr)

    c = np.array([1, -2, -2])
    marking, value = max_reachable_marking(P, bdd, c)
    assert marking == None
