from random import choice
from math import inf

from .Keys import U, R, T

def reset_utility(G):
    for n in G.nodes:
        G.nodes[n][U] = 0

def create_random_policy(G):
    pi = {} 
    for n in G:
        pi[n] = choice(list(G.neighbors(n)))

    return pi

def create_policy_from_utility(G):
    pi = {}
    for n in G:
        best_u = -inf
        best_n = None

        for n_p in G.neighbors(n):
            u = G.nodes[n_p][U]
            if u > best_u:
                best_u = u
                best_n = n_p

        pi[n] = best_n

    return pi

def run_policy(G, pi, start, max_steps):
    states = [start]
    rewards = [G.nodes[start][R]]

    for _ in range(max_steps):
        if G.nodes[start][T]:
            break
        
        start = pi[start]
        states.append(start)
        rewards.append(G.nodes[start][R])

    return states, rewards