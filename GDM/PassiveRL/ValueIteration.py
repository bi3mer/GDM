from networkx import set_node_attributes

from ..utility import reset_utility, create_policy_from_utility
from ..Keys import U, R, P

def __in_place_value_iteration(G, max_iteration, gamma, theta):
    for _ in range(max_iteration):
        delta = 0

        for n in G:
            r = G.nodes[n][R]
            u = r + gamma*max(G.edges[(n, n_p)][P] * G.nodes[n_p][U] for n_p in G.neighbors(n))
            delta = max(delta, abs(G.nodes[n][U] - u))
            G.nodes[n][U] = u

        if delta < theta:
            break

def __value_iteration(G, max_iteration, gamma, theta):
    for _ in range(max_iteration):
        delta = 0
        u_temp = {}

        for n in G:
            r = G.nodes[n][R]
            u = r + gamma * max(G.edges[(n, n_p)][P] * G.nodes[n_p][U] for n_p in G.neighbors(n))
            delta = max(delta, abs(G.nodes[n][U] - u))

            u_temp[n] = {U: u}

        set_node_attributes(G, u_temp)

        if delta < theta:
            break

def value_iteration(G, max_iteration, gamma, theta, in_place=False, should_reset_utility=True):
    if should_reset_utility:
        reset_utility(G)

    if in_place:
        __in_place_value_iteration(G, max_iteration, gamma, theta)
    else:
        __value_iteration(G, max_iteration, gamma, theta)

    return create_policy_from_utility(G)
