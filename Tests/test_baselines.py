from random import random
from GDM.Graph import Graph
from GDM.Baseline import random_policy, greed_policy

def test_random():
    G = Graph()
    G.add_default_node('1')
    G.add_default_node('2')
    G.add_default_node('3')
    G.add_default_node('4', terminal=True)

    G.add_default_edge('1', '2')
    G.add_default_edge('2', '3')
    G.add_default_edge('2', '4')
    G.add_default_edge('3', '4')

    pi = random_policy(G)

    assert pi['1'] == '2'
    assert pi['3'] == '4'
    three_found = False
    four_found = False


    for i in range(100):
        three_found |= pi['2'] == '3'
        four_found |= pi['2'] == '4'
        
        if three_found and four_found:
            break

        pi = random_policy(G)

    assert three_found
    assert four_found

def test_greedy():
    G = Graph()
    G.add_default_node('1')
    G.add_default_node('2', reward=2)
    G.add_default_node('3', reward=-1, terminal=True)
    G.add_default_node('4', reward=-10, terminal=True)
    G.add_default_node('5', reward=-100, terminal=True)

    G.add_default_edge('1', '2')
    G.add_default_edge('1', '3')

    G.add_default_edge('2', '4')
    G.add_default_edge('2', '5')

    pi = greed_policy(G)

    assert pi['1'] == '2'
    assert '3' not in pi
    assert pi['2'] == '4'
    assert '4' not in pi
    assert '5' not in pi