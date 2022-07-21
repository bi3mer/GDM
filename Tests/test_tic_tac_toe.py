from GDM.Graph import Graph
from GDM.utility import *
from GDM import ADP

from typing import List, Tuple

BASE_REWARD = 0
WIN_REWARD = 1.0
DRAW_REWARD = 0.0
LOSS_REWARD = -1.0
X = 'X'
O = 'O'
E = '-'

GAMMA = 1.0

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
    return not any(val == E for val in board)

def reward(board: Tuple[int]) -> Tuple[bool, int]:
    for i, j, k in WIN_CONDITIONS:
        if board[i] != E and board[i] == board[j] and board[j] == board[k]:
            return True, WIN_REWARD if board[i] == X else LOSS_REWARD

    if board_is_full(board):
        return True, DRAW_REWARD

    return False, BASE_REWARD

def __build_opposing_policy(G: Graph, queue: List[Tuple[str]], update_r):
    G_ = Graph()
    for b in queue:
        G_.add_default_node(b, reward=0)

    while len(queue) > 0:
        # Get possible moves for the agent
        cur = queue.pop()
        actions = G.neighbors(cur) # Possible moves for the agent
        for tgt_state in actions:
            tgt_node = G.get_node(tgt_state)
            if not G_.has_node(tgt_state):
                G_.add_default_node(tgt_state, reward=update_r(tgt_node.reward), terminal=tgt_node.is_terminal)
            if not G_.has_edge(cur, tgt_state):
                G_.add_default_edge(cur, tgt_state, [(tgt_state, 1.0)])

            if tgt_node.is_terminal:
                continue
            
            # Get possible responses
            potential_states = tgt_node.neighbors # Possible responses
            likelihood = 1 / len(potential_states)

            # if there is a state where the opponent can win, select that
            found_terminal = False
            for s_p in potential_states:
                s_p_node = G.get_node(s_p)
                if s_p_node.is_terminal:
                    found_terminal = True
                    if not G_.has_node(s_p):
                        G_.add_default_node(s_p, reward=update_r(s_p_node.reward), terminal=True)

                    if not G_.has_edge(tgt_state, s_p):
                        G_.add_default_edge(tgt_state, s_p, [(s_p, 1.0)])
    
                    break
            
            if found_terminal:
                continue

            # otherwise, the player is random
            for s_p in potential_states:
                s_p_node = G.get_node(s_p)
                if not G_.has_node(s_p):
                    G_.add_default_node(s_p, reward=update_r(s_p_node.reward), terminal=s_p_node.is_terminal)

                if not G_.has_edge(tgt_state, s_p):
                    G_.add_default_edge(tgt_state, s_p, [(s_p_p, likelihood) for s_p_p in potential_states])
    
                if not s_p_node.is_terminal:
                    queue.append(s_p)
    
    return G_


def __build_tic_tac_toe_graph() -> Tuple[Tuple[str], Graph, Graph]:
    # build full tic-tac-toe  graph
    G = Graph()
    B = (E,E,E, E,E,E, E,E,E)
    queue: List[Tuple[int, Tuple[int]]] = [(X, B)] # turn, board, reward
    G.add_default_node(queue[0][1], reward=BASE_REWARD)

    while len(queue) > 0:
        turn_marker, board = queue.pop() 
        next_turn_marker = O if turn_marker == 'X' else X

        for i in range(len(board)):
            if board[i] == E:
                new_board = [val for val in board]
                new_board[i] = turn_marker
                new_board = tuple(new_board)

                if new_board not in G.nodes:
                    assert new_board not in G.nodes

                    game_over, r = reward(new_board)

                    G.add_default_node(new_board, reward=r, terminal=game_over)
                    G.add_default_edge(board, new_board)

                    if not game_over:
                        queue.append((next_turn_marker, new_board))
                else:
                    G.add_default_edge(board, new_board)
    
    # build graph for x-player where o-player is stochastic in its choices
    queue = [B]
    G_X = __build_opposing_policy(G, queue, lambda r: r)
  
    # build graph for o-player where x-player is stochastic in its choices
    queue = [b for b in G.neighbors(B)]
    G_O = __build_opposing_policy(G, queue, lambda r: -r)

    return B, G, G_X, G_O

start, G, G_X, G_O = __build_tic_tac_toe_graph()

def test_board_is_full():
    assert board_is_full((E,X)) == False
    assert board_is_full((X,E)) == False
    assert board_is_full((X,X)) == True

    assert board_is_full((E,O)) == False
    assert board_is_full((O,E)) == False
    assert board_is_full((O,O)) == True

def test_reward():
    assert reward((O,X,E, E,X,O, E,X,E)) == (True, WIN_REWARD)
    assert reward((X,O,X, O,X,O, X,O,X)) == (True, WIN_REWARD)
    assert reward((X,X,O, X,O,O, X,O,X)) == (True, WIN_REWARD)
    assert reward((E, O, X, O, E, X, E, E, X)) == (True, WIN_REWARD)
    assert reward((X,X,E, O,O,O, E,E,X)) == (True, LOSS_REWARD)
    assert reward((X,X,O, O,O,X, X,O,X)) == (True, DRAW_REWARD)
    
    assert reward((E,X,E, E,E,E, E,E,O)) == (False, BASE_REWARD)
    assert reward((E,O,E, O,X,O, X,O,X)) == (False, BASE_REWARD)

    assert reward((O,X,X, X,E,X, O,O,O)) == (True, LOSS_REWARD)
    assert reward((E,X,X, X,E,E, O,O,O)) == (True, LOSS_REWARD)
    assert reward((O,X,X, X,E,X, O,O,O)) == (True, LOSS_REWARD)

    assert reward((E,E,O, X,O,X, O,E,X,)) == (True, LOSS_REWARD)
    
def print_board(board: Tuple[int]):
    for i in range(3):
        mod = i*3
        print(board[mod], board[1 + mod], board[2 + mod])

def print_policy_choices(G_: Graph, pi, cur):
    print(f'R={G_.reward(cur)}, U={G_.utility(cur)}')
    choosen = 0
    for i, n in enumerate(G_.neighbors(cur)):
        print(f'\t{i}) {n}, {G_.reward(n)}, {G_.utility(n)}, {calculate_utility(G_, cur, n, GAMMA)}')
        if n == pi[cur]:
            choosen = i
    print(f'\tWent with: {choosen}')
    print(G_.get_edge(cur, pi[cur]).probability)

def play_game(pi_x, pi_o,):
    print('//////////////////////////////////////////////')
    cur = start
    
    for cur in G.neighbors(start):
        print_board(cur)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        x_turn = False
        current_reward = BASE_REWARD
        while not G.get_node(cur).is_terminal:
            if x_turn:
                print('X')
                print_policy_choices(G_X, pi_x, cur)
                cur = pi_x[cur]
            else:
                print('O')
                print_policy_choices(G_O, pi_o, cur)
                cur = pi_o[cur]

            x_turn = not x_turn
            game_over, current_reward = reward(cur)
            assert game_over == G.get_node(cur).is_terminal

            print_board(cur)
            print('============')

        print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
        assert current_reward == DRAW_REWARD
        assert game_over == True

def test_policy_iteration_vs_value_iteration():
    pi_x_pi = ADP.policy_iteration(G_X, 1.0)
    pi_o_vi = ADP.value_iteration(G_O, 5_000, 1.0, 1e-16)
    play_game(pi_x_pi, pi_o_vi)

def test_in_place_value_iteration_vs_modified_in_place_policy_iteration():
    pi_x_vi = ADP.value_iteration(G_X, 5_000, 1.0, 1e-16)
    pi_o_pi_ip_m = ADP.policy_iteration(G_O, 1.0, in_place=True, modified=True)
    play_game(pi_x_vi, pi_o_pi_ip_m)

def modified_in_place_policy_iteration_vs_in_place_value_iteration():
    pi_x_pi_ip_m = ADP.policy_iteration(G_X, 1.0, in_place=True, modified=True)
    pi_o_vi_ip = ADP.value_iteration(G_O, 5_000, 1.0, 1e-16, in_place=False)
    play_game(pi_x_pi_ip_m, pi_o_vi_ip)

def test_in_place_value_iteration_vs_policy_iteration():
    pi_x_vi_ip = ADP.value_iteration(G_X, 5_000, 1.0, 1e-16, in_place=True)
    pi_o_pi = ADP.policy_iteration(G_O, 1.0)
    play_game(pi_x_vi_ip, pi_o_pi)

def test_modified_policy_iteration_vs_in_place_policy_iteration():
    pi_x_pi_m = ADP.policy_iteration(G_X, 1.0, modified=True)
    pi_o_pi_ip = ADP.policy_iteration(G_O, 1.0, in_place=True)
    play_game(pi_x_pi_m, pi_o_pi_ip)

def test_in_place_policy_iteration_vs_modified_policy_Iteration():
    pi_x_pi_ip = ADP.policy_iteration(G_X, 1.0, in_place=True)
    pi_o_pi_m = ADP.policy_iteration(G_O, 1.0, modified=True)
    play_game(pi_x_pi_ip, pi_o_pi_m)
