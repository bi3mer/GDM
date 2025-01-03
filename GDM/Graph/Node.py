from dataclasses import dataclass
from typing import Set, Dict, Any

@dataclass
class Node:
    name: str
    reward: float
    utility: float
    is_terminal: bool
    neighbors: Set[str]

    def to_dictionary(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'reward': self.reward,
            'utility': self.utility,
            'is-terminal': self.is_terminal
        } # self.neighbors is reconstructed from edges