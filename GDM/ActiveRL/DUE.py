from ..utility import create_policy_from_utility

def initialize_for_direct_utility_estimation(G):
    for n in G.nodes:
        node = G.nodes[n]
        node[U] = 0
        node[SUM] = 0
        node[VC] = 0

def direct_utility_estimation(G, gamma, states, rewards):
    utility = gamma * sum(rewards)

    for s in states:
        node = G.nodes[s]
        node[SUM] += utility
        node[VC] += 1
        node[U] = node[SUM] / node[VC]

    return create_policy_from_utility(G)