from lib2to3.pytree import Node
from GDM.Graph import Graph
from GDM.utility import calculate_max_utility
from tests import test_gamblers_ruin
from GDM import ADP

import matplotlib.pyplot as plt

GAMMA = 1.0
THETA = 1e-16
N = 200

G = test_gamblers_ruin.build_gamblers_ruin()

# pi = ADP.value_iteration(G, N, GAMMA, THETA)
pi = ADP.value_iteration(G, N, GAMMA, THETA, in_place=True)
# pi = ADP.policy_iteration(G,GAMMA)
# pi = ADP.policy_iteration(G,GAMMA, modified=True)
# pi = ADP.policy_iteration(G,GAMMA, modified=True, in_place=True)

bet = [val-key for key, val in pi.items()]
utilities = [G.utility(n) for n in G.nodes if not G.get_node(n).is_terminal]
# utilities = [calculate_max_utility(G, n, GAMMA) for n in G.nodes if not G.get_node(n).is_terminal]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,4))
ax1.plot([i for i in range(len(bet))], bet)
ax2.plot([i for i in range(len(utilities))], utilities)

plt.show()
