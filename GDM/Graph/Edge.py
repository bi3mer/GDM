from dataclasses import dataclass
from typing import Any, Dict, Tuple, List

@dataclass
class Edge:
    src: str
    tgt: str
    probability: List[Tuple[str, float]]

    def to_dictionary(self) -> Dict[str, Any]:
        return {
            'src': self.src,
            'tgt': self.tgt,
            'probability': self.probability
        }