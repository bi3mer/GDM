from dataclasses import dataclass, field
from typing import Set

@dataclass
class Node:
    name: str
    reward: float
    utility: float
    is_terminal: bool

    # NOTE: I would rather this be of type Set but I can't figure out how to
    # get the dataclass to work. It changes it to type list and it's very
    # annoying.
    neighbors: Set[str]