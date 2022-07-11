# from networkx import set_node_attributes
from typing import Dict
from math import inf
from ..Graph import Graph

from ..utility import create_random_policy, reset_utility

######################## Policy Evaluation ########################
def __modified_in_place_policy_evaluation(G: Graph, pi: Dict[str, str], gamma: float, policy_k: int):
    for __ in range(policy_k):
        for n in G.nodes:
            r = G.get_node(n).reward
            u = sum([p_val*G.get_node(n_true).utility for n_true, p_val in G.edges[(n, pi[n])].probability.items()])
            G.nodes[n].utility = r + gamma * u

def __modified_policy_evaluation(G: Graph, pi: Dict[str, str], gamma: float, policy_k: int):
    for __ in range(policy_k):
        u_temp: Dict[str, float] = {}
        for n in G.nodes:
            r = G.nodes[n].reward
            u = sum([p_val*G.nodes[n_true].utility for n_true, p_val in G.edges[(n, pi[n])].probability.items()])
            u_temp[n] = r + gamma*u
        
        G.set_node_utilities(u_temp)

def __in_place_policy_evaluation(G: Graph, _, gamma: float, policy_k: int):
    for __ in range(policy_k):
        for n in G.nodes:
            r = G.nodes[n].reward
            u = max(sum([p_val*G.nodes[n_true].utility for n_true, p_val in G.edges[(n, n_p)].probability.items()]) for n_p in G.neighbors(n))
            G.nodes[n].utility = r + gamma * u

def __policy_evaluation(G: Graph, _, gamma: float, policy_k: int):
    for __ in range(policy_k):
        u_temp: Dict[str, float] = {}
        for n in G.nodes:
            r = G.nodes[n].reward
            u = max(sum([p_val*G.nodes[n_true].utility for n_true, p_val in G.edges[(n, n_p)].probability.items()]) for n_p in G.neighbors(n))
            u_temp[n] = r + gamma*u
        
        G.set_node_utilities(u_temp)

######################## Policy Improvement ########################
def __policy_improvement(G: Graph, pi: Dict[str, str]) -> bool:
    changed = False
    for n in G.nodes:
        old = pi[n]

        best_s = None
        best_u = -inf
        for n_p in G.neighbors(n):
            u_p = G.nodes[n_p].utility
            if u_p > best_u:
                best_s = n_p
                best_u = u_p

        if old != best_s:
            pi[n] = best_s
            changed = True

    return changed

######################## Policy Iteration ########################
def policy_iteration(G: Graph, gamma: float, modified: bool=False, 
                     in_place: bool=False, policy_k: int=10, 
                     should_reset_utility: bool=True) -> Dict[str, str]:
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
