from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Edge:
    src: str
    tgt: str
    probability: Dict[str, float] = field(default_factory=dict)