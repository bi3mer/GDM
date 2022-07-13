from GDM.ActiveRL import DUE
from GDM import PassiveRL
from GDM.Graph import Graph
from GDM.utility import *

from random import seed

MAX_X = 4
MAX_Y = 3

GAMMA = 1.0
THETA = 1e-15
N = 1_000

def __make_key(x: int, y: int):
    return f'{y}_{x}'

def __build_grid_world(reward: float):
    '''
    This is the more complex version of grid world where the agent may try
    to go one direction but will randomly go another. I am hard coding this
    version because I'll be testing the policy's directly since there is 
    only one correct answer.
    '''
    g = Graph() 

    # create nodes
    for y in range(MAX_Y):
        for x in range(MAX_X):
            # ignore the blank position
            if y == 1 and x == 1:
                continue

            # create node and its reward
            src = __make_key(x, y)
            if x == MAX_X - 1 and y == MAX_Y - 1:
                g.add_default_node(src, terminal=True)
            elif x == MAX_X - 1 and y == MAX_Y - 2:
                g.add_default_node(src, reward=-1, terminal=True)
            else:
                g.add_default_node(src, reward=reward)

    for src in g.nodes:
        # get name
        y, x = [int(i) for i in src.split('_')]
        valid_targets = []

        # create left connection
        if x - 1 >= 0 and not (x - 1 == 1 and y == 1):
            valid_targets.append(__make_key(x-1, y))
        else:
            valid_targets.append(src)

        # create right connection
        if x + 1 < MAX_X and not (x + 1 == 1 and y == 1):
            valid_targets.append(__make_key(x+1, y))
        else:
            valid_targets.append(src)

        # create up connection
        if y - 1 >= 0 and not (x == 1 and y - 1 == 1):
            valid_targets.append(__make_key(x, y-1))
        else:
            valid_targets.append(src)

        # create down connection
        if y + 1 < MAX_Y and not (x == 1 and y + 1 == 1):
            valid_targets.append(__make_key(x, y+1))
        else:
            valid_targets.append(src)

        sub_probability = 0.2 / (len(valid_targets)-1)
        for tgt in valid_targets:
            p = []
            tgt_not_used = True
            for p_tgt in valid_targets:
                p.append((p_tgt, 0.8 if tgt == p_tgt and tgt_not_used else sub_probability))
                if tgt == p_tgt:
                    tgt_not_used = False
            
            g.add_default_edge(src, tgt, p)

    return '0_0', g

def __display_utility_table(G):
    print('--------' * MAX_X + '-')
    for y in reversed(range(MAX_Y)):
        out = '| '
        for x in range(MAX_X):
            if x == 1 and y == 1:
                out += '      |'
            else:
                key = __make_key(x, y)
                # out +=  '{:.2f} | '.format(G.get_node(key).utility)
                out +=  '{:.3f} | '.format(G.reward(key) + calculate_max_utility(G, key))
        
        print(out)
        print('--------' * MAX_X + '-')

def __small_positive_reward_tester(rl_lambda):
    seed(0)
    start, G = __build_grid_world(0.05)
    pi = rl_lambda(G)
    assert pi != None

    # __display_utility_table(G)

    states, rewards = run_policy(G, start, pi, 30)

    print('here')

    assert len(states) == 31
    assert len(states) == len(rewards)

    print('still here')

def __large_positive_reward_tester(rl_lambda):
    seed(0)
    start, G = __build_grid_world(0.6)
    pi = rl_lambda(G)
    assert pi != None

    states, rewards = run_policy(G, start, pi, 50)
    assert len(states) == 51
    assert len(states) == len(rewards)

def __small_negative_reward_tester(rl_lambda):
    seed(0)
    _, G = __build_grid_world(-0.01)
    pi = rl_lambda(G)
    assert pi != None

    # __display_utility_table(G)

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
    assert pi['1_2'] == '2_2'

def __medium_negative_reward_tester(rl_lambda):
    seed(0)
    _, G = __build_grid_world(-0.1)
    pi = rl_lambda(G)
    assert pi != None

    # __display_utility_table(G)

    # going up from start to terminal node
    assert pi['0_0'] == '1_0'
    assert pi['1_0'] == '2_0'
    assert pi['2_0'] == '2_1'
    assert pi['2_1'] == '2_2'
    assert pi['2_2'] == '2_3'

    # going right from start
    assert pi['0_1'] == '0_2'
    assert pi['0_2'] == '1_2'
    assert pi['0_3'] == '0_2'
    assert pi['1_2'] == '2_2'

def __very_negative_reward_tester(rl_lambda):
    seed(0)
    _, G = __build_grid_world(-1.5)
    pi = rl_lambda(G)
    assert pi != None

    # __display_utility_table(G)

    # going up from start to terminal node
    assert pi['0_0'] == '0_1'
    assert pi['1_0'] == '2_0'
    assert pi['2_0'] == '2_1'
    assert pi['2_1'] == '2_2'
    assert pi['2_2'] == '2_3'

    # going right from start
    assert pi['0_1'] == '0_2'
    assert pi['0_2'] == '1_2'
    assert pi['0_3'] == '1_3'
    assert pi['1_2'] == '1_3'

##### Value Iteration
value_iteration_lambda = lambda G: PassiveRL.value_iteration(G, N, GAMMA, THETA)

def test_value_iteration_small_positive_reward():
    __small_positive_reward_tester(value_iteration_lambda)

def test_value_iteration_large_positive_reward():
    __large_positive_reward_tester(value_iteration_lambda)

def test_value_iteration_small_negative_reward():
    __small_negative_reward_tester(value_iteration_lambda)

def test_value_iteration_medium_negative_reward():
    __medium_negative_reward_tester(value_iteration_lambda)

def test_value_iteration_very_negative_reward():
    __very_negative_reward_tester(value_iteration_lambda)

# ##### In-Place Value Iteration
in_place_value_iteration_lambda = lambda G: PassiveRL.value_iteration(G, N, GAMMA, THETA, in_place=True)

def test_in_place_value_iteration_small_positive_reward():
    __small_positive_reward_tester(in_place_value_iteration_lambda)

def test_in_place_value_iteration_large_positive_reward():
    __large_positive_reward_tester(in_place_value_iteration_lambda)

def test_in_place_value_iteration_small_negative_reward():
    __small_negative_reward_tester(in_place_value_iteration_lambda)

def test_in_place_value_iteration_medium_negative_reward():
    __medium_negative_reward_tester(in_place_value_iteration_lambda)

def test_in_place_value_iteration_very_negative_reward():
    __very_negative_reward_tester(in_place_value_iteration_lambda)

##### Policy Iteration
policy_iteration_lambda = lambda G: PassiveRL.policy_iteration(G, GAMMA)

def test_policy_iteration_small_positive_reward():
    __small_positive_reward_tester(policy_iteration_lambda)

def test_policy_iteration_large_positive_reward():
    __large_positive_reward_tester(policy_iteration_lambda)

def test_policy_iteration_small_negative_reward():
    __small_negative_reward_tester(policy_iteration_lambda)

def test_policy_iteration_medium_negative_reward():
    __medium_negative_reward_tester(policy_iteration_lambda)

def test_policy_iteration_very_negative_reward():
    __very_negative_reward_tester(policy_iteration_lambda)

##### In-Place Policy Iteration
in_place_policy_iteration_lambda = lambda G: PassiveRL.policy_iteration(G, GAMMA, in_place=True)

def test_in_place_policy_iteration_small_positive_reward():
    __small_positive_reward_tester(in_place_policy_iteration_lambda)

def test_in_place_policy_iteration_large_positive_reward():
    __large_positive_reward_tester(in_place_policy_iteration_lambda)

def test_in_place_policy_iteration_small_negative_reward():
    __small_negative_reward_tester(in_place_policy_iteration_lambda)

def test_in_place_policy_iteration_medium_negative_reward():
    __medium_negative_reward_tester(in_place_policy_iteration_lambda)

def test_in_place_policy_iteration_very_negative_reward():
    __very_negative_reward_tester(in_place_policy_iteration_lambda)

##### Modified Policy Iteration
modified_policy_iteration_lambda = lambda G: PassiveRL.policy_iteration(G, GAMMA, modified=True)

def test_modified_policy_iteration_small_positive_reward():
    __small_positive_reward_tester(modified_policy_iteration_lambda)

def test_modified_policy_iteration_large_positive_reward():
    __large_positive_reward_tester(modified_policy_iteration_lambda)

def test_modified_policy_iteration_small_negative_reward():
    __small_negative_reward_tester(modified_policy_iteration_lambda)

def test_modified_policy_iteration_medium_negative_reward():
    __medium_negative_reward_tester(modified_policy_iteration_lambda)

def test_modified_policy_iteration_very_negative_reward():
    __very_negative_reward_tester(modified_policy_iteration_lambda)

##### Modified In-Place Policy Iteration
modified_in_place_policy_iteration_lambda = lambda G: PassiveRL.policy_iteration(G, GAMMA, in_place=True, modified=True)

def test_modified_in_place_policy_iteration_small_positive_reward():
    __small_positive_reward_tester(modified_in_place_policy_iteration_lambda)

def test_modified_in_place_policy_iteration_large_positive_reward():
    __large_positive_reward_tester(modified_in_place_policy_iteration_lambda)

def test_modified_in_place_policy_iteration_small_negative_reward():
    __small_negative_reward_tester(modified_in_place_policy_iteration_lambda)

def test_modified_in_place_policy_iteration_medium_negative_reward():
    __medium_negative_reward_tester(modified_in_place_policy_iteration_lambda)

def test_modified_in_place_policy_iteration_very_negative_reward():
    __very_negative_reward_tester(modified_in_place_policy_iteration_lambda)