from GDM import RL
from GDM.Graph import Graph, Node
from GDM.utility import *

from typing import List, Tuple
from random import seed

BASE_REWARD = 0.5
EMPTY = 0

WIN_CONDITIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

def board_is_full(board: Tuple[int]) -> bool:
    return not any(val == 0 for val in board)

def reward(board: Tuple[int]) -> int:
    for i, j, k in WIN_CONDITIONS:
        if board[i] != EMPTY and board[i] == board[j] and board[j] == board[k]:
            return board[i]
    return BASE_REWARD

def __build_tic_tac_toe_graph():
    G = Graph()
    queue: List[Tuple[int, Tuple[int], int]] = [(1, (0,0,0, 0,0,0, 0,0,0), BASE_REWARD)] # turn, board, reward
    G.add_default_node(queue[0][1], reward=BASE_REWARD)
    start = queue[0][1]

    while len(queue) > 0:
        turn_marker, board, r = queue.pop() 
        next_turn_marker = 1 if turn_marker == -1 else -1

        for i in range(len(board)):
            if board[i] == EMPTY:
                new_board = [val for val in board]
                new_board[i] = turn_marker
                new_board = tuple(new_board)

                if new_board not in G.nodes:
                    r = reward(new_board)
                    is_terminal = r!=BASE_REWARD or board_is_full(new_board)

                    G.add_default_node(new_board, reward=r, terminal=is_terminal)
                    G.add_default_edge(board, new_board, [(new_board, 1.0)])

                    if not is_terminal:
                        queue.append((next_turn_marker, new_board, r))
                else:
                    G.add_default_edge(board, new_board, [(new_board, 1.0)])

    return start, G

start, G = __build_tic_tac_toe_graph()

def test_board_is_full():
    assert board_is_full((0,1)) == False
    assert board_is_full((1,0)) == False
    assert board_is_full((1,1)) == True

    assert board_is_full((0,-11)) == False
    assert board_is_full((-11,0)) == False
    assert board_is_full((-1,-1)) == True

def test_board():
    assert G.reward((-1,1,0, 0,1,-1, 0,1,0)) == 1
    assert G.reward((1,-1,1, -1,1,-1, 1,-1,1)) == 1
    assert G.reward((1,1,-1, 1,-1,-1, 1,-1,1)) == 1
    assert G.reward((1,1,0, -1,-1,-1, 0,0,1)) == -1
    assert G.reward((0,1,0, 0,0,0, 0,0,-1)) == BASE_REWARD
    assert (1,1,0, 0,0,0, 0,0,0) not in G.nodes

def conv(val: int) -> str:
    if val == 0: return '-'
    elif val == 1: return 'X'
    return 'O'

def print_board(board: Tuple[int]):
    for i in range(3):
        mod = i*3
        print(conv(board[mod]), conv(board[1 + mod]), conv(board[2 + mod]))

def reset_utility(node: Node) -> None:
    node.utility = 0

def test_value_iteration():
    # NOTE: I could use the reset utility option but I want to test the map function
    G.map_nodes(reset_utility)

    pi_x = RL.policy_iteration(G, 0.9)
    # pi_x = RL.value_iteration(G, 0.9, 1.0, 1e-16)
    pi_o = create_policy_from_utility(G, 0.9, maximize=False)

    # pi_o = RL.policy_iteration(G, 0.9)

    print('//////////////////////////////////////////////')
    cur = start
    for cur in G.neighbors(start):
        x_turn = False
        current_reward = BASE_REWARD
        while current_reward == BASE_REWARD and not board_is_full(cur):
            if x_turn:
                cur = pi_x[cur]
            else:
                cur = pi_o[cur]

            x_turn = not x_turn
            current_reward = reward(cur)

            print_board(cur)
            print('============')

        print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')

        # assert current_reward == 0
        # assert board_is_full(cur)
    assert False
    