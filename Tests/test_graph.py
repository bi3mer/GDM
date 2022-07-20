from dataclasses import dataclass
import pytest
from GDM.Graph import Graph, Node, Edge

def test_get_node():
    G = Graph()
    G.add_default_node('1')
    assert G.get_node('1').name == '1'
    with pytest.raises(KeyError):
        G.get_node('2')

def test_add_node():
    @dataclass
    class TestNode(Node):
        test: int

    G = Graph()
    G.add_node(Node('1', 1.9, 1.0, False, set()))
    
    n = G.get_node('1')
    assert n.name == '1'
    assert n.reward == 1.9
    assert n.utility == 1.0
    assert n.is_terminal == False

    with pytest.raises(AssertionError):
        G.add_node('21')

    with pytest.raises(AssertionError):
        G.add_node('1')


    G.add_node(TestNode('2', 1.0, 2.0, True, set(), 12))
    assert G.get_node('2').test == 12

def test_remove_node():
    G = Graph()
    G.add_default_node('2')

    with pytest.raises(KeyError):
        G.remove_node('1')

    G.remove_node('2')
    assert '2' not in G.nodes
    assert len(G.nodes) == 0

def test_get_edge():
    G = Graph()
    G.add_default_node('1')
    G.add_default_node('2')
    G.add_default_edge('1','2')

    assert ('1','2') in G.edges
    assert G.get_edge('1','2').tgt == '2'

def test_custom_edge():
    @dataclass
    class CustomEdge(Edge):
        q: int

    G = Graph()
    with pytest.raises(AssertionError):
        G.add_edge('1')

    G.add_default_node('1')
    G.add_default_node('2')
    G.add_edge(CustomEdge('1', '2', [('2', 1.0)], 3))

    assert ('1', '2') in G.edges
    assert len(G.edges) == 1
    assert G.get_edge('1', '2').q == 3
    assert '2' in G.get_node('1').neighbors


def test_remove_edge():
    G = Graph()
    G.add_default_node('a')
    G.add_default_node('b')
    G.add_default_edge('a', 'b')
    assert len(G.edges) == 1
    
    G.remove_edge('a', 'b')
    assert len(G.edges) == 0

def test_neighbors():
    G = Graph()
    G.add_default_node('1')
    G.add_default_node('2')
    G.add_default_node('3')
    
    G.add_default_edge('1', '2')
    G.add_default_edge('1', '3')
    G.add_default_edge('2', '3')

    assert '2' in G.neighbors('1')
    assert '3' in G.neighbors('1')
    assert len(G.neighbors('1')) == 2

    assert '3' in G.neighbors('2')
    assert len(G.neighbors('2')) == 1

    assert len(G.neighbors('3')) == 0

def test_set_node_utilities():
    G = Graph()
    for i in range(10):
        G.add_default_node(str(i), utility=i)

    new_utility_values = {}
    for i in range(10):
        new_utility_values[str(i)] = 0
        assert G.utility(str(i)) == i

    G.set_node_utilities(new_utility_values)

    for i in range(10):
        assert G.utility(str(i)) == 0

def test_map_nodes():
    G = Graph()
    for i in range(10):
        G.add_default_node(str(i))

    def modifier(n: Node):
        n.reward = 10
        n.is_terminal = True

    G.map_nodes(modifier)

    for i in range(10):
        key = str(i)
        assert G.reward(key) == 10
        assert G.is_terminal(key) == True

# def reward(self, node_name: str) -> float:
#     return self.nodes[node_name].reward

# def is_terminal(self, node_name: str) -> bool:
#     return self.nodes[node_name].is_terminal

# def map_nodes(self, func: Callable[[Node], None]):
#     for n in self.nodes.values():
#         func(n)