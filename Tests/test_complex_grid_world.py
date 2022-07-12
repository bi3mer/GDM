from logging.config import valid_ident
from GDM.ActiveRL import DUE
from GDM import PassiveRL
from GDM.Graph import Graph
from GDM.utility import *

from random import seed

def __build_grid_world():
    '''
    This is the more complex version of grid world where the agent may try
    to go one direction but will randomly go another. I am hard coding this
    version because I'll be testing the policy's directly since there is 
    only one correct answer.
    '''
    MAX_X = 4
    MAX_Y = 3
    g = Graph() 

    # create nodes
    for y in range(MAX_Y):
        for x in range(MAX_X):
            # ignore the blank position
            if y == 1 and x == 1:
                continue

            # create node and its reward
            src = f'{y}_{x}'
            if x == MAX_X - 1 and y == MAX_Y - 1:
                g.add_default_node(src, terminal=True)
            elif x == MAX_X - 1 and y == MAX_Y - 2:
                g.add_default_node(src, reward=-1, terminal=True)
            else:
                g.add_default_node(src, reward=-0.04)


    for src in g.nodes:
        # get name
        y, x = [int(i) for i in src.split('_')]
        valid_targets = []

        # create left connection
        if x - 1 >= 0 and not (x - 1 == 1 and y == 1):
            valid_targets.append(f'{y}_{x-1}')

        # create right connection
        if x + 1 < MAX_X and not (x + 1 == 1 and y == 1):
            valid_targets.append( f'{y}_{x+1}')

        # create up connection
        if y - 1 >= 0 and not (x == 1 and y - 1 == 1):
            valid_targets.append(f'{y-1}_{x}')

        # create down connection
        if y + 1 < MAX_Y and not (x == 1 and y + 1 == 1):
            valid_targets.append(f'{y+1}_{x}')

        # check if solid block is a neighbor
        if (x-1 == 1 and y == 1) or (x+1 == 1 and y == 1) or \
           (x == 1 and y-1 == 1) or (x == 1 and y+1 == 1):
            
            # solid block just uses a turn, doesn't move the agent.
            valid_targets.append(src) 

        sub_probability = 0.2 / (len(valid_targets)-1)
        for tgt in valid_targets:
            p = {}
            for p_tgt in valid_targets:
                p[p_tgt] = 0.8 if tgt == p_tgt else sub_probability
            
            g.add_default_edge(src, tgt, p)

    return '0_0', g

def __is_optimal_policy(pi):
    # going up from start to terminal node
    assert pi['0_0'] == '1_0'
    assert pi['1_0'] == '2_0'
    assert pi['2_0'] == '2_1'
    assert pi['2_1'] == '2_2'
    assert pi['2_2'] == '2_3'

    # going right from start
    assert pi['0_1'] == '0_0'
    assert pi['0_2'] == '0_1'
    assert pi['0_3'] == '0_2'
    assert pi['1_1'] == '2_1'

# def test_policy_iteration():
#     seed(0)
#     start, G = __build_grid_world()

#     pi = PassiveRL.policy_iteration(G, 0.8)
#     assert pi != None
#     __is_optimal_policy(pi)


#     states, rewards = run_policy(G, start, pi, 50)
#     assert len(states) >= 6
#     assert len(states) == len(rewards)
#     assert rewards[-1] == 1
#     assert states[-1] == '2_3'

# def test_modified_in_place_policy_iteration():
#     seed(0)
#     start, G = __build_grid_world()
#     pi = PassiveRL.policy_iteration(G, 0.9, modified=True, in_place=True)
#     assert pi != None
#     # __is_optimal_policy(pi)

#     states, rewards = run_policy(G, start, pi, 50)
#     assert len(states) >= 6
#     assert len(states) == len(rewards)
#     assert rewards[-1] == 1 or rewards[-1] == -1
#     assert states[-1] == '2_3'


def test_value_iteration():
    GAMMA = 1.0
    THETA = 1e-15
    N = 1_000
    seed(0)

    start, G = __build_grid_world()
    pi = PassiveRL.value_iteration(G, N, GAMMA, THETA)
    assert pi != None
    __is_optimal_policy(pi)

    states, rewards = run_policy(G, start, pi, 50)
    assert len(states) >= 6
    assert len(states) == len(rewards)
    assert rewards[-1] == 1 or rewards[-1] == -1
    assert states[-1] == '2_3'






    # g.add_default_edge('0_0', '1_0', {'1_0': 0.8, '0_1': 0.2})
    # g.add_default_edge('0_0', '0_1', {'0_1': 0.8, '1_0': 0.2})

    # g.add_default_edge('1_0', '2_0', {'2_0': 0.8, '0_0': 0.2})
    # g.add_default_edge('1_0', '0_0', {'0_0': 0.8, '2_0': 0.2})

    # g.add_default_edge('2_0', '3_0', {'3_0': 0.8, '1_0': 0.2})
    # g.add_default_edge('2_0', '1_0', {'1_0': 0.8, '3_0': 0.2})

    # g.add_default_edge('3_0', '3_1', {'3_1': 0.8, '2_0': 0.2})
    # g.add_default_edge('3_0', '2_0', {'2_0': 0.8, '3_1': 0.2})

    # g.add_default_edge('3_1', '3_2', {'3_2': 0.8, '3_0': 0.2})
    # g.add_default_edge('3_1', '3_0', {'3_0': 0.8, '3_2': 0.2})

    # g.add_default_edge('3_2', '3_3', {'3_3': 0.8, '3_1': 0.1, '2_2': 0.1})
    # g.add_default_edge('3_2', '3_1', {'3_1': 0.8, '3_3': 0.1, '2_2': 0.1})
    # g.add_default_edge('3_2', '2_2', {'2_2': 0.8, '3_3': 0.1, '3_1': 0.1})