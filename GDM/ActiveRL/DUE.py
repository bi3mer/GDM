from typing import List, Dict

from ..utility import create_policy_from_utility
from ..Graph import Graph

def direct_utility_estimation(G: Graph, gamma: float, states: List[str], rewards: List[float]) -> Dict[str, str]:
    utility = gamma * sum(rewards)

    for s in states:
        node = G.get_node(s)
        node.reward_sum += utility
        node.times_visited += 1
        node.utility = node.reward_sum / node.times_visited

    return create_policy_from_utility(G)