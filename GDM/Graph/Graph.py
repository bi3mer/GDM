from typing import Callable, Set, Dict, List, Tuple
from .Edge import Edge
from .Node import Node

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

    ##### Node Operations
    def get_node(self, node_name: str) -> Node:
        return self.nodes[node_name]

    def add_node(self, node: Node):
        assert isinstance(node) == Node
        assert node.name not in self.nodes
        self.nodes[node.name] = node

    def add_default_node(self, node_name: str, reward: float=1.0, utility: float=0.0, 
                         terminal: bool=False, neighbors: Set[str]=None):

        assert node_name not in self.nodes
        if neighbors == None:
            neighbors = set()

        self.nodes[node_name] = Node(node_name, reward, utility, terminal, neighbors)

    def remove_node(self, node_name: str):
        del self.nodes[node_name]

    ##### Edge Operations
    def get_edge(self, src_name: str, tgt_name: str) -> Edge:
        return self.edges[(src_name, tgt_name)]

    def add_edge(self, edge: Edge):
        # assert edge.src in self.nodes
        # assert edge.tgt in self.nodes
        # assert (edge.src, edge.tgt) not in self.edges
        self.edges[(edge.src, edge.tgt)] = edge
        
        neighbors = self.nodes[edge.src].neighbors
        if edge.tgt not in neighbors:
            neighbors.add(edge.tgt)

    def add_default_edge(self, src_name: str, tgt_name: str, p: List[Tuple[str, float]]=None):
        if p == None:
            p = []

        self.add_edge(Edge(src_name, tgt_name, p))

    def remove_edge(self, src_node, tgt_node):
        del self.edges[(src_node, tgt_node)]

    ##### Useful Functions
    def neighbors(self, node_name: str) -> Set[str]:
        return self.nodes[node_name].neighbors

    def set_node_utilities(self, utilities: Dict[str, float]):
        for node_name, utility in utilities.items():
            self.nodes[node_name].utility = utility

    def utility(self, node_name: str) -> float:
        return self.nodes[node_name].utility

    def reward(self, node_name: str) -> float:
        return self.nodes[node_name].reward

    def is_terminal(self, node_name: str) -> bool:
        return self.nodes[node_name].is_terminal

    def map_nodes(self, func: Callable[[Node], None]):
        for n in self.nodes.values():
            func(n)
