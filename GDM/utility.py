from typing import Dict, List, Tuple
from random import choice, random
from math import inf

from .Graph import Graph, Node

def expected_utility_sum(g: Graph, n: str, n_p: str) -> float:
    return sum(p_p*g.get_node(p_n).utility for p_n, p_p in g.get_edge(n, n_p).probability)

def max_expected_utility_sum(g: Graph, n: str) -> float:
    return max(expected_utility_sum(g, n, n_p) for n_p in g.neighbors(n))

# def calculate_utility(g: Graph, src: Node, gamma: float):
#     R = src.reward
#     N = src.name
#     calc_u = lambda prob, n_tgt: prob*g.get_node(n_tgt).reward
#     neighbor_u = lambda n_p: [calc_u(prob, n_tgt) for n_tgt, prob in g.get_edge(N, n_p).probability]
#     return R + gamma*max(sum(neighbor_u(n_p)) for n_p in g.neighbors(N))

def calculate_utility(G: Graph, n: Node, gamma: float) -> float:

    vals = []
    for n_p in G.neighbors(n.name):
        Q = []
        for n_tgt, prob in G.get_edge(n.name, n_p).probability:
            # Q.append(n.reward + prob * gamma * G.utility(n_tgt))
            # Q.append(prob * (n.reward + gamma * G.utility(n_p)))
            node = G.get_node(n_tgt)
            Q.append(prob * (node.reward + node.utility))

        vals.append(sum(Q))

    return n.reward + gamma*max(vals)
    # return max(vals)

def reset_utility(G: Graph):
    for n in G.nodes:
        G.nodes[n].utility = 0

def create_random_policy(G: Graph) -> Dict[str, str]:
    pi: dict[str, str] = {} 
    for n in G.nodes:
        pi[n] = choice(list(G.neighbors(n)))

    return pi

def create_policy_from_utility(G: Graph, gamma: float) -> Dict[str, str]:
    pi: Dict[str, str] = {}
    for n in G.nodes:
        best_u = -inf
        best_n: str

        for n_p in G.neighbors(n):
            u = calculate_utility(G, G.get_node(n_p), gamma)
            # u = G.get_node(n_p).utility
            if u > best_u:
                best_u = u
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

def run_epsilon_greedy_utility_policy(
        G: Graph, start: str, pi: Dict[str, str], epsilon: float, 
        max_steps: int) -> Tuple[List[str], List[float]]:
        
    states = [start]
    rewards = [G.get_node(start).reward]
    cur_state = start

    for _ in range(max_steps):
        if G.nodes[cur_state].is_terminal:
            break
        
        if random() < epsilon:
            tgt_state = choice(list(G.get_node(cur_state).neighbors))
        else:
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