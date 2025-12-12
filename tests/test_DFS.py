import numpy as np
from src.PetriNet import PetriNet
from src.DFS import dfs_reachable

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

    output= dfs_reachable(PetriNet(P, T, P, T, I, O, M0))

    expected = {
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    }

    assert output == expected, f"Expected {expected}, but got {output}"

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

    output= dfs_reachable(PetriNet(P, T, P, T, I, O, M0))

    expected = {
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1)
    }

    assert output == expected, f"Expected {expected}, but got {output}"

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

    output= dfs_reachable(PetriNet(P, T, P, T, I, O, M0))

    expected = {
        (1, 1, 1),
    }

    assert output == expected, f"Expected {expected}, but got {output}"

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

    output= dfs_reachable(PetriNet(P, T, P, T, I, O, M0))

    expected = {
        (1, 1, 1),
    }

    assert output == expected, f"Expected {expected}, but got {output}"

def test_004():
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
    M0 = np.array([1, 0, 0, 0, 0, 0, 0])

    output= dfs_reachable(PetriNet(P, T, P, T, I, O, M0))

    expected = {
        (0, 0, 0, 0, 0, 0, 1),
        (0, 0, 0, 1, 0, 1, 0),
        (0, 0, 0, 1, 1, 0, 0),
        (0, 0, 1, 0, 0, 1, 0),
        (0, 0, 1, 0, 1, 0, 0),
        (0, 1, 0, 0, 0, 1, 0),
        (0, 1, 0, 0, 1, 0, 0),
        (1, 0, 0, 0, 0, 0, 0),
    }

    assert output == expected, f"Expected {expected}, but got {output}"

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

    output= dfs_reachable(PetriNet(P, T, P, T, I, O, M0))

    expected = {
        (0, 0, 0, 0, 0, 1, 1),
        (0, 0, 0, 0, 1, 0, 1),
        (0, 0, 0, 1, 1, 1, 0),
        (0, 0, 1, 0, 1, 1, 0),
        (0, 1, 0, 0, 1, 1, 0),
        (1, 0, 0, 0, 0, 1, 0),
    }

    assert output == expected, f"Expected {expected}, but got {output}"
