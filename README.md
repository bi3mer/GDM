#  Graph-based Sequential Decision Making (GSDM)

The goal of this library is to provide out of the box active and passive reinforcement learning algorithms that are easy to use. The work on your part is to define your problem as a [networkx directed graph](https://networkx.org/documentation/stable/reference/classes/digraph.html) and the library takes care of the rest.

## Examples and Tests

Each file in [tests](./tests) builds a sample game and runs every algorithm in the library. To test, run `pytest`.

### Grid World

[tests/test_grid_world.py](./tests/test_grid_world.py) shows how the game Grid World can be formulated as a networkx graph with the topmost function `__build_grid_world`. For every node, you must define the node's reward and if the node is terminal. Note, you should use [Keys](./GSDM/Keys.py) to avoid magic strings. For every edge, define the probability that the next state will actually be the target node. In the case of Grid World, the probability is always 100% so `1.0` is assigned for each edge—which is to say that the environment is deterministic.

