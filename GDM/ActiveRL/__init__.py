from . import DUE
from .QLearning import q_learning
from .SARSA import sarsa
from ..utility import run_policy


# def train(rl, G, start, iterations, max_steps):
#     for _ in range(n):
#         pi = rl(G)
#         states, rewards = run_policy(G, pi, start, max_steps)
#         DUE.direct_utility_estimation(G, 0.6, states, rewards)
#         if rewards[-1] == 1:
#             break
