from GDM import ADP
from GDM.Graph import Graph
from GDM.utility import *

"""
There are many optimal policies so I can't test for a specific one. (For more on
this, see: https://medium.com/@jaems33/gamblers-problem-b4e91040e58a.) Instead,
we test for a coin flip where heads is very likely and we know that the policy
has to be risk averse. Meaning, it will never willingly risk transitioning to the
losing node 0.

Also: https://github.com/AdamOlsson/rl_gamblers_problem
"""

GAMMA = 1.0
THETA = 1e-10
N = 200

SIZE = 100
COIN_FLIP = 0.75 # probability of heads

def build_gamblers_ruin() -> Graph:
    G = Graph()

    G.add_default_node(0, reward=0, terminal=True)
    for i in range(1, SIZE):
        G.add_default_node(i, reward=0)
    G.add_default_node(SIZE, reward=1, terminal=True)

    for i in range(1, SIZE):
        for j in range(1, i+1):
            win_state = i+j
            loss_state = i-j
            if loss_state < 0 or win_state > SIZE:
                continue

            G.add_default_edge(i, win_state, [(win_state, COIN_FLIP), (loss_state, 1-COIN_FLIP)])

    return G

G = build_gamblers_ruin()

def __test_policy(pi: Dict[str, str]):
    for src in range(2, SIZE):
        tgt = pi[src]
        edge = G.get_edge(src, tgt)
        for n_p, p in edge.probability:
            assert n_p != 0


def test_value_iteration():
    pi = ADP.value_iteration(G, N, GAMMA, THETA)
    __test_policy(pi)

def test_in_place_value_iteration():
    pi = ADP.value_iteration(G, N, GAMMA, THETA, in_place=True)
    __test_policy(pi)


def test_policy_iteration():
    pi = ADP.policy_iteration(G, GAMMA)
    __test_policy(pi)

def test_in_place_policy_iteration():
    pi = ADP.policy_iteration(G, GAMMA, in_place=True)
    __test_policy(pi)

def test_modified_policy_iteration():
    pi = ADP.policy_iteration(G, GAMMA, modified=True)
    __test_policy(pi)

def test_in_place_modified_policy_iteration():
    pi = ADP.policy_iteration(G, GAMMA, in_place=True, modified=True)
    __test_policy(pi)

    



    