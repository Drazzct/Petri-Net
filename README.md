# Symbolic and Algebraic Reasoning in 1-Safe Petri Nets

## Project Overview

This software implements a formal verification suite for **1-Safe Petri Nets**. It combines explicit state-space exploration with symbolic model checking techniques to analyze concurrency, reachability, and correctness properties of distributed systems.

The core objective is to bridge the gap between graph-theoretic models (Petri Nets) and algebraic reasoning (Boolean logic and Linear Programming). It addresses the "state space explosion" problem by utilizing **Binary Decision Diagrams (BDDs)** for compact state representation.

## Features & Algorithms

### 1. PNML Parsing

- **Functionality:** Parses standard .pnml files (ISO/IEC 15909-2) to construct an internal matrix-based representation (I and O incidence matrices).
- **Validation:** Automatically enforces 1-safe properties during loading.

### 2. Explicit Reachability Analysis (BFS)

- **Method:** Breadth-First Search.
- **Description:** Enumerates every possible marking by firing enabled transitions layer-by-layer. This provides a baseline for verifying the correctness of symbolic results and measuring performance (Time/Memory).

### 3. Symbolic Reachability (BDDs)

- **Method:** Fixed-Point Iteration.
- **Description:** Encodes the Petri Net's state space into Boolean functions.
- **Variables:** Uses interleaved variable ordering (x, x') for transition relations.
- **Process:** Iteratively computes the new reachability set (Union of Current Set and Next States) until the set stabilizes.
- **Visualization:** Renders the resulting BDD structure to a PNG image using Graphviz.

### 4. Deadlock Detection (Hybrid Approach)

- **Method:** BDD Reachability + Integer Linear Programming (ILP).
- **Description:**

  1.  Uses the BDD to generate potentially unsafe reachable markings.
  2.  Solves an ILP optimization problem (using `PuLP`) for each candidate to mathematically prove if any transitions are enabled.

  - **Constraint:** Maximize transition firing subject to token availability.

### 5. Reachability Optimization

- **Method:** Linear Optimization over Symbolic State Space.
- **Objective:** Find a reachable marking M that maximizes c^T \* M for a given weight vector c.
- **Optimization:** Iterates directly over the valid paths of the BDD rather than the entire universe of possible states (2^n), ensuring efficiency even for large nets.

---

Installation & Setup
Prerequisites

Python 3.8+

1. Create Virtual Environment

Navigate to the project root in your terminal/command prompt and create a virtual environment.

Windows

py -m venv venv
venv\Scripts\activate


macOS / Linux

python3 -m venv venv
source venv/bin/activate

2. Install Dependencies

Upgrade pip and install all required libraries:

python -m pip install --upgrade pip setuptools wheel
python -m pip install numpy pyeda graphviz pulp

How to Run
Run with a specific file (Recommended)

To analyze a specific Petri net file, run:

python main.py test3.pnml


### Expected Output

The console will display performance metrics for each task:

```text
--- 1. Parsing PNML ---Loaded: 12 places, 12 transitions.--- 2. Explicit Reachability (BFS) ---Total reachable states (BFS): 27Execution Time : 0.001200 secondsPeak Memory    : 0.045000 MB--- 3. BDD Reachability ---Total reachable states (BDD): 27Execution Time : 0.071200 secondsPeak Memory    : 0.095000 MB[SUCCESS] BDD visualization saved to 'bdd.png'.--- 4. Deadlock Detection ---Result: No deadlock reachable.--- 5. Optimization ---Max Value  : 5Max Marking: [1, 0, 0, 1, 0, 0, ...]
```

## Project Structure

```text
├── main.py                # Entry point: Orchestrates all analysis tasks├── requirements.txt       # Python dependencies (numpy, pyeda, pulp, graphviz)├── test3.pnml             # Sample Petri Net model (Token Ring)├── bdd.png                # Output: Visualization of the reachable state space├── README.md              # Project documentation└── src/                   # Source code package    ├── PetriNet.py        # Data structures and XML parsing logic    ├── BFS.py             # Explicit state exploration algorithms    ├── BDD.py             # Symbolic state exploration using PyEDA    ├── Deadlock.py        # Deadlock detection logic (ILP integration)    └── Optimization.py    # Optimization algorithms over BDDs
```
