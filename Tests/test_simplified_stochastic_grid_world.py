from GDM.ActiveRL import DUE
from GDM import PassiveRL
from GDM.Keys import *
import GDM
from networkx import DiGraph

def __is_solid_block(x,y):
    return x == 1 and y == 1

def __build_grid_world(MAX_X, MAX_Y):
    '''
    This is a simplified version of stochastic grid world where 20% of the time
    the agent will not move. The more common version is 80% of the time the 
    action is successful and the remaining percent will to to other actions.
    '''
    g = DiGraph() 

    for y in range(MAX_Y):
        for x in range(MAX_X):
            # ignore the blank position
            if y == 1 and x == 1:
                continue

            # create node and its reward
            src = f'{y}_{x}'
            g.add_node(src)
            if x == MAX_X - 1 and y == MAX_Y - 1:
                g.nodes[src][R] = 1
                g.nodes[src][T] = True
            elif x == MAX_X - 1 and y == MAX_Y - 2:
                g.nodes[src][R] = -1
                g.nodes[src][T] = True
            else:
                g.nodes[src][R] = -0.05
                g.nodes[src][T] = False

            # create left connection
            if x - 1 >= 0 and not __is_solid_block(x-1, y):
                tgt = f'{y}_{x-1}'
                g.add_edge(src, tgt)


                g.edges[(src, tgt)][P] = {tgt: 0.8, src: 0.2}

            # create right connection
            if x + 1 < MAX_X and not __is_solid_block(x+1, y):
                tgt = f'{y}_{x+1}'
                g.add_edge(src, tgt)
                g.edges[(src, tgt)][P] = {tgt: 0.8, src: 0.2}

            # create up connection
            if y - 1 >= 0  and not __is_solid_block(x, y-1):
                tgt = f'{y-1}_{x}'
                g.add_edge(src, tgt)
                g.edges[(src, tgt)][P] = {tgt: 0.8, src: 0.2}

            # create down connection
            if y + 1 < MAX_Y and not __is_solid_block(x, y+1):
                tgt = f'{y+1}_{x}'
                g.add_edge(src, tgt)
                g.edges[(src, tgt)][P] = {tgt: 0.8, src: 0.2}

    return '0_0', g


def test_policy_iteration():
    start, G = __build_grid_world(5, 5)
    pi = PassiveRL.policy_iteration(G, 0.6)
    assert pi != None
    states, rewards = GDM.run_policy(G, pi, start, 20)
    assert len(states) >= 9
    assert len(states) <= 20
    assert len(rewards) == len(states)
    assert rewards[-1] == 1
    assert states[-1] == '4_4'

def test_in_place_policy_iteration():
    start, G = __build_grid_world(20, 20)
    pi = PassiveRL.policy_iteration(G, 0.5, in_place=True)
    assert pi != None
    states, rewards = GDM.run_policy(G, pi, start, 100)
    assert len(states) >= 39
    assert len(states) <= 100
    assert len(states) == len(rewards)
    assert rewards[-1] == 1
    assert states[-1] == '19_19'

def test_modified_policy_iteration():
    start, G = __build_grid_world(30, 30)
    pi = PassiveRL.policy_iteration(G, 0.7, modified=True)
    assert pi != None
    states, rewards = GDM.run_policy(G, pi, start, 100)
    assert len(states) >= 59
    assert len(rewards) <= 100
    assert len(states) == len(rewards)
    assert rewards[-1] == 1
    assert states[-1] == '29_29'

def test_modified_in_place_policy_iteration():
    start, G = __build_grid_world(25, 25)
    pi = PassiveRL.policy_iteration(G, 0.9, modified=True, in_place=True)
    assert pi != None
    states, rewards = GDM.run_policy(G, pi, start, 100)
    assert len(states) >= 21
    assert len(states) <= 100
    assert len(states) == len(rewards)
    assert rewards[-1] == 1
    assert states[-1] == '24_24'

def test_value_iteration():
    start, G = __build_grid_world(5, 10)
    pi = PassiveRL.value_iteration(G, 100, 0.8, 1e-13, in_place=False)
    assert pi != None
    states, rewards = GDM.run_policy(G, pi, start, 100)
    assert len(states) >= 14
    assert len(states) <= 100
    assert len(states) == len(rewards)
    assert rewards[-1] == 1
    assert states[-1] == '9_4'

def test_in_place_value_iteration():
    start, G = __build_grid_world(8, 10)
    pi = PassiveRL.value_iteration(G, 100, 0.8, 1e-13, in_place=True)
    assert pi != None
    states, rewards = GDM.run_policy(G, pi, start, 100)
    assert len(states) >= 17
    assert len(states) <= 100
    assert len(states) == len(rewards)
    assert rewards[-1] == 1
    assert states[-1] == '9_7'

def test_direct_utility_estimation():
    start, G = __build_grid_world(4, 3)
    DUE.initialize_for_direct_utility_estimation(G)

    for _ in range(200):
        pi = GDM.create_policy_from_utility(G)
        states, rewards = GDM.run_policy(G, pi, start, 40)
        DUE.direct_utility_estimation(G, 0.6, states, rewards)
        if rewards[-1] == 1:
            break

    assert len(states) >= 6
    assert len(states) <= 100
    assert len(states) == len(rewards)
    assert rewards[-1] == 1
    assert states[-1] == '2_3'