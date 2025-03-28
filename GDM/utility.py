from typing import Dict, List, Tuple
from random import choice, random
from math import inf
from typing import Optional

from .Graph import Graph

def calculate_utility(G: Graph, src: str, tgt: str, gamma: float) -> float:
    return sum(prob * (G.reward(n_tgt) + gamma*G.utility(n_tgt)) for n_tgt, prob in G.get_edge(src, tgt).probability)

def calculate_max_utility(G: Graph, n: str, gamma: float) -> List[Tuple[str, float]]:
    node = G.get_node(n)
    if node.is_terminal:
        return 0

    return max(calculate_utility(G, n, n_p, gamma) for n_p in node.neighbors)

def reset_utility(G: Graph):
    for n in G.nodes:
        G.nodes[n].utility = 0

def create_random_policy(G: Graph) -> Dict[str, str]:
    pi: dict[str, str] = {}
    for n in G.nodes:
        if not G.get_node(n).is_terminal:
            pi[n] = choice(list(G.neighbors(n)))

    return pi

def create_policy(G: Graph, gamma: float) -> Dict[str, str]:
    pi: Dict[str, str] = {}
    for n in G.nodes:
        if G.get_node(n).is_terminal:
            continue

        best_u = -inf
        best_n: str

        for n_p in G.neighbors(n):
            u = calculate_utility(G, n, n_p, gamma)

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

# Return [error, path]. Error is true if there was an error.
def bfs(G: Graph, src: str, tgt: str) -> Optional[List[str]]:
    if src == tgt:
        return []

    queue = [src]
    came_from = {}
    path_found = False

    while len(queue) > 0 and not path_found:
        cur = queue.pop(0)

        for next in G.neighbors(cur):
            if next == tgt:
                came_from[tgt] = cur
                path_found = True
                break

            if next in came_from:
                continue

            came_from[next] = cur
            queue.append(next)

    if path_found:
        path = []
        cur = tgt
        while cur != src:
            path.append(cur)
            cur = came_from[cur]

        return path

    return None

