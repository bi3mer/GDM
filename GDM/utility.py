from typing import Dict, List, Tuple
from random import choice, random
from math import inf

from .Graph import Graph

def calculate_utility(G: Graph, src: str, tgt: str) -> float:
    return sum(prob * (G.utility(n_tgt) + G.reward(n_tgt)) for n_tgt, prob in G.get_edge(src, tgt).probability)

def calculate_max_utility(G: Graph, n: str) -> float:
    # print(n, G.get_node(n).is_terminal, G.reward(n))
    return max(calculate_utility(G, n, n_p) for n_p in G.neighbors(n))

def reset_utility(G: Graph):
    for n in G.nodes:
        G.nodes[n].utility = 0

def create_random_policy(G: Graph) -> Dict[str, str]:
    pi: dict[str, str] = {} 
    for n in G.nodes:
        if not G.get_node(n).is_terminal:
            pi[n] = choice(list(G.neighbors(n)))

    return pi

def create_policy_from_utility(G: Graph, gamma: float, maximize: bool=True) -> Dict[str, str]:
    pi: Dict[str, str] = {}
    for n in G.nodes:
        if maximize:
            best_u = -inf
        else: 
            best_u = inf

        best_n: str

        for n_p in G.neighbors(n):
            if G.get_node(n_p).is_terminal:
                u = G.reward(n_p)
            else:
                u = G.reward(n_p) + gamma * calculate_max_utility(G, n_p)
     
            if maximize: 
                if u > best_u:
                    best_u = u
                    best_n = n_p
            elif u < best_u:
                best_u = u
                best_n = n_p

        pi[n] = best_n

    return pi

def create_policy_from_q_values(G: Graph) -> Dict[str, str]:
    pi: Dict[str, str] = {}
    for n in G.nodes:
        best_q = -inf
        best_n: str

        for n_p in G.neighbors(n):
            q = G.get_edge(n, n_p).q
            if q > best_q:
                best_q = q
                best_n = n_p

        pi[n] = best_n

    return pi

def run_policy(G: Graph, start: str, pi: Dict[str, str], max_steps: int) -> Tuple[List[str], List[float]]:
    states = [start]
    rewards = [G.nodes[start].reward]
    cur_state = start

    for _ in range(max_steps):
        if G.nodes[cur_state].is_terminal:
            break
        
        tgt_state = pi[cur_state]
        p = random()
        for next_state, probability in G.get_edge(cur_state, tgt_state).probability:
            if p <= probability:
                tgt_state = next_state
                break
            else:
                p -= probability

        states.append(tgt_state)
        rewards.append(G.nodes[tgt_state].reward)
        cur_state = tgt_state

    return states, rewards