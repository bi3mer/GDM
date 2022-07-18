from GDM import ADP
from GDM.Graph import Graph
from GDM.utility import *

from random import seed

def __build_grid_world(MAX_X, MAX_Y):
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
                g.add_default_node(src, reward=1, terminal=True)
            elif x == MAX_X - 1 and y == MAX_Y - 2:
                g.add_default_node(src, reward=-1.0, terminal=True)
            else:
                g.add_default_node(src, reward=-0.04)

    # create edges
    for src in g.nodes:
        # get name
        y, x = [int(i) for i in src.split('_')]

        # create left connection
        if x - 1 >= 0 and not (x - 1 == 1 and y == 1):
            tgt = f'{y}_{x-1}'
            g.add_default_edge(src, tgt, [(tgt, 1.0)])

        # create right connection
        if x + 1 < MAX_X and not (x + 1 == 1 and y == 1):
            tgt = f'{y}_{x+1}'
            g.add_default_edge(src, tgt, [(tgt, 1.0)])

        # create up connection
        if y - 1 >= 0 and not (x == 1 and y - 1 == 1):
            tgt = f'{y-1}_{x}'
            g.add_default_edge(src, tgt, [(tgt, 1.0)])

        # create down connection
        if y + 1 < MAX_Y and not (x == 1 and y + 1 == 1):
            tgt = f'{y+1}_{x}'
            g.add_default_edge(src, tgt, [(tgt, 1.0)])

    return '0_0', g

def __display_utility_table(G, MAX_X, MAX_Y):
    print()
    print('--------' * MAX_X + '-')
    for y in reversed(range(MAX_Y)):
        out = '| '
        for x in range(MAX_X):
            if x == 1 and y == 1:
                out += '      |'
            else:
                key = f'{y}_{x}'
                out +=  '{:.2f} | '.format(G.get_node(key).utility)
        
        print(out)
        print('--------' * MAX_X + '-')

def test_policy_iteration():
    seed(0)
    start, G = __build_grid_world(5, 5)
    pi = ADP.policy_iteration(G, 0.6)
    assert pi != None
    states, rewards = run_policy(G, start, pi, 30)

    assert rewards[-1] == 1
    assert len(states) == 9
    assert len(rewards) == 9
    assert states[-1] == '4_4'

def test_in_place_policy_iteration():
    start, G = __build_grid_world(20, 20)
    pi = ADP.policy_iteration(G, 0.5, in_place=True)
    assert pi != None
    states, rewards = run_policy(G, start, pi,100)
    assert rewards[-1] == 1
    assert len(states) == 39
    assert len(rewards) == 39
    assert states[-1] == '19_19'

def test_modified_policy_iteration():
    seed(0)
    start, G = __build_grid_world(30, 30)
    pi = ADP.policy_iteration(G, 0.7, modified=True)
    assert pi != None
    
    states, rewards = run_policy(G, start, pi, 100)
    assert rewards[-1] == 1
    assert len(states) == 59
    assert len(rewards) == 59
    assert states[-1] == '29_29'

def test_modified_in_place_policy_iteration():
    start, G = __build_grid_world(15, 15)
    pi = ADP.policy_iteration(G, 0.9, modified=True, in_place=True)
    assert pi != None

    states, rewards = run_policy(G, start, pi, 100)
    assert rewards[-1] == 1
    assert len(states) == 29
    assert len(states) ==  len(rewards)
    assert states[-1] == '14_14'

def test_value_iteration():
    seed(0)
    start, G = __build_grid_world(5, 10)
    pi = ADP.value_iteration(G, 100, 0.8, 1e-13, in_place=False)
    assert pi != None

    states, rewards = run_policy(G, start, pi, 100)
    assert rewards[-1] == 1
    assert len(states) == 14
    assert len(states) == len(rewards)
    assert states[-1] == '9_4'

def test_in_place_value_iteration():
    seed(0)
    start, G = __build_grid_world(8, 10)
    pi = ADP.value_iteration(G, 100, 0.8, 1e-13, in_place=True)
    assert pi != None

    states, rewards = run_policy(G, start, pi, 100)
    assert rewards[-1] == 1
    assert len(states) == 17
    assert len(rewards) == 17
    assert states[-1] == '9_7'
