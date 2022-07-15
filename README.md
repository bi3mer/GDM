#  Graph-based Decision Making (GDM)

The goal of this library is to provide out of the box passive reinforcement learning algorithms that are easy to use. The work on your part is to define your problem as a [Graph](./GDM/Graph/Graph.py) and the library takes care of the rest. The use of a graph, rather than the classic [MDP](https://en.wikipedia.org/wiki/Markov_decision_process) formulation of `S,A,R,P`, is to more easily accommodate problems where the list of possible actions is large and varied possible states. The graph ends up being a more convenient structure, in my opinion.

## Examples and Tests

Each file in [tests](./tests) builds a sample problem and runs every algorithm in the library. To test, run `pytest`.

### Grid World

Will update this towards the end of the initial implementation.

#### Deterministic 

[tests/test_deterministic_grid_world.py](./tests/test_deterministic_grid_world.py) shows how the game [Grid World](https://inst.eecs.berkeley.edu/~cs188/fa18/assets/slides/lec9/FA18_cs188_lecture9_MDPs_II_6pp.pdf) can be formulated as a graph with the topmost function `__build_grid_world`. For every node, you must define the node's reward and if the node is terminal. For every edge, define the probability that the next state will actually be the target node. In the case of deterministic Grid World, the probability is always 100% so `1.0` is assigned for each edge.

### Simplified Stochastic

TBA

### Complex

TBA

### Tic-Tac-Toe
TBA