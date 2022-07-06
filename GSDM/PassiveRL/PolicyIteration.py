from networkx import set_node_attributes
from math import inf

from ..utility import create_random_policy, reset_utility
from ..Keys import U, R, P

######################## Policy Evaluation ########################
def __modified_in_place_policy_evaluation(G, pi, gamma, policy_k):
    for __ in range(policy_k):
        for n in G:
            r = G.nodes[n][R]
            n_p = pi[n]
            u = G.edges[(n, n_p)][P] *G.nodes[n_p][U]
            G.nodes[n][U] = r + gamma * u

def __modified_policy_evaluation(G, pi, gamma, policy_k):
    for __ in range(policy_k):
        u_temp = {}
        for n in G:
            r = G.nodes[n][R]
            n_p = pi[n]
            u = G.edges[(n, n_p)][P] * G.nodes[n_p][U]
            u_temp[n] = {U: r + gamma*u}
        
        set_node_attributes(G, u_temp)

def __in_place_policy_evaluation(G, _, gamma, policy_k):
    for __ in range(policy_k):
        for n in G:
            r = G.nodes[n][R]
            u = max(G.edges[(n, n_p)][P] * G.nodes[n_p][U] for n_p in G.neighbors(n)) 
            G.nodes[n][U] = r + gamma * u

def __policy_evaluation(G, _, gamma, policy_k):
    for __ in range(policy_k):
        u_temp = {}
        for n in G:
            r = G.nodes[n][R]
            u = max(G.edges[(n, n_p)][P] * G.nodes[n_p][U] for n_p in G.neighbors(n)) 
            u_temp[n] = {U: r + gamma*u}
        
        set_node_attributes(G, u_temp)

######################## Policy Improvement ########################
def __policy_improvement(G, pi):
    changed = False
    for n in G:
        old = pi[n]

        best_s = None
        best_u = -inf
        for n_p in G.neighbors(n):
            u_p = G.nodes[n_p][U]
            if u_p > best_u:
                best_s = n_p
                best_u = u_p

        if old != best_s:
            pi[n] = best_s
            changed = True

    return changed

######################## Policy Iteration ########################
def policy_iteration(G, gamma, modified=False, in_place=False, policy_k=10, should_reset_utility=True):
    # reset utility
    if should_reset_utility:
        reset_utility(G) 

    # make random policy
    pi = create_random_policy(G)

    # get the policy eval based on input arguments
    if modified and in_place:
        policy_eval = __modified_in_place_policy_evaluation
    elif modified and not in_place:
        policy_eval = __modified_policy_evaluation
    elif not modified and in_place:
        policy_eval = __in_place_policy_evaluation
    else:
        policy_eval = __policy_evaluation

    # run policy iteration
    while True:
        policy_eval(G, pi, gamma, policy_k)
        changed = __policy_improvement(G, pi)
        if not changed:
            break

    return pi
