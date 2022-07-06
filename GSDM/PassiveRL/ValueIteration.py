from networkx import set_node_attributes

from .utility import reset_utility, create_policy
from .Keys import U, R, P

def __in_place_value_iteration(G, max_iteration, gamma, theta):
    for _ in range(max_iteration):
        delta = 0

        for n in G:
            R = G.nodes[n][R]
            u = R + gamma * max(G.nodes[n_p][P] * G.nodes[n_p][U] for n_p in G.neighbors(n))
            G.nodes[n][U] = u

            delta = max(delta, abs(G.nodes[n][U] - u))

        if delta < theta:
            break

def __value_iteration(G, max_iteration, gamma, theta):
    for _ in range(max_iteration):
        delta = 0
        u_temp = {}

        for n in G:
            r = G.nodes[n][R]
            u = r + gamma * max(G.nodes[n_p][P] * G.nodes[n_p][U] for n_p in G.neighbors(n))
            u_temp[n] = {U: u}

            delta = max(delta, abs(G.nodes[n][U] - u))

        set_node_attributes(G, u_temp)

        if delta < theta:
            break

def value_iteration(G, max_iteration, gamma, theta, in_place=True, should_reset_utility=True):
    if should_reset_utility:
        reset_utility()

    if in_place:
        __in_place_value_iteration(G, max_iteration, gamma, theta)
    else:
        __value_iteration(G, max_iteration, gamma, theta)

    return create_policy(G)

