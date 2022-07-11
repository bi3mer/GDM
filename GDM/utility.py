from random import choice, random
from math import inf
from typing import Dict

from .Graph import Graph

def reset_utility(G: Graph):
    for n in G.nodes:
        G.nodes[n].utility = 0

def create_random_policy(G: Graph):
    pi: dict[str, str] = {} 
    for n in G.nodes:
        pi[n] = choice(list(G.neighbors(n)))

    return pi

def create_policy_from_utility(G: Graph):
    pi = {}
    for n in G.nodes:
        best_u = -inf
        best_n = None

        for n_p in G.neighbors(n):
            u = G.nodes[n_p].utility
            if u > best_u:
                best_u = u
                best_n = n_p

        pi[n] = best_n

    return pi

def run_policy(G: Graph, pi: Dict[str, str], start: str, max_steps: int):
    states = [start]
    rewards = [G.nodes[start].reward]
    cur_state = start

    for _ in range(max_steps):
        if G.nodes[cur_state].is_terminal:
            break
        
        tgt_state = pi[cur_state]
        p = random()
        for next_state, probability in G.get_edge(cur_state, tgt_state).probability.items():
            if p <= probability:
                tgt_state = next_state
                break
            else:
                p -= probability

        states.append(tgt_state)
        rewards.append(G.nodes[tgt_state].reward)
        cur_state = tgt_state

    return states, rewards