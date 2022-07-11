from dataclasses import dataclass, field
from typing import Set

@dataclass
class Node:
    name: str
    reward: float
    utility: float
    is_terminal: bool
    neighbors: Set[str]

    # direct utility estimation
    reward_sum: int = 0
    times_visited: int = 0