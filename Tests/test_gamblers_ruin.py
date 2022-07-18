from GDM import ADP
from GDM.Graph import Graph
from GDM.utility import *


GAMMA = 1.0
THETA = 1e-32
N = 200

# https://github.com/dennybritz/reinforcement-learning/blob/master/DP/Gamblers%20Problem%20Solution.ipynb
SIZE = 100
COIN_FLIP = 0.4 # probability of heads
OPTIMAL_POLICY = [
    0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25, 25, 30, 32, 34, 36, 25, 
    40, 42, 25, 46, 48, 50, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 76, 
    50, 50, 50, 84, 50, 88, 50, 92, 94, 96, 98, 100, 52, 54, 56, 58, 60, 62, 
    64, 66, 68, 70, 72, 74, 76, 75, 75, 75, 84, 75, 88, 75, 92, 94, 96, 98, 100, 
    77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 100, 100, 100, 100, 100, 100, 
    100, 100, 100, 100, 100, 100
]

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

# G = __build_gamblers_ruin()

# def __equivalent_policies(pi: Dict[str, str]):
#     out = ''
#     for i in range(1, SIZE):
#         out = f'{out} || {i} :: {pi[i]}'
#         # out = f'{out} || {i} :: {pi[i]} =?= {OPTIMAL_POLICY[i]}'
#     print(out)

#     for i in range(1,SIZE):
#         if i > 14 and i < 20:
#             continue
#         print(f'{i} :: {pi[i]} == {OPTIMAL_POLICY[i]}')
#         assert pi[i] == OPTIMAL_POLICY[i]

# # def test_value_iteration():
# #     pi = ADP.value_iteration(G, N, GAMMA, THETA)
# #     __equivalent_policies(pi)

# def test_in_place_value_iteration():
#     pi = ADP.value_iteration(G, N, GAMMA, THETA)
#     __equivalent_policies(pi)


# # def test_policy_iteration():
# #     pi = ADP.policy_iteration(G, GAMMA)
# #     __equivalent_policies(pi)

# # def test_in_place_policy_iteration():
# #     pi = ADP.policy_iteration(G, GAMMA, in_place=True)
# #     __equivalent_policies(pi)

# # def test_modified_policy_iteration():
# #     pi = ADP.policy_iteration(G, GAMMA, modified=True)
# #     __equivalent_policies(pi)

# # def test_in_place_modified_policy_iteration():
# #     pi = ADP.policy_iteration(G, GAMMA, in_place=True, modified=True)
# #     __equivalent_policies(pi)

    



    