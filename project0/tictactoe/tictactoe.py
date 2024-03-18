"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, column = action
    if row < 0 or row > 3 or column < 0 or column > 3:
        raise ValueError("Action out of bounds")
    if board[row][column] is not EMPTY:
        raise ValueError("Action is not valid for board")
    new_board = copy.deepcopy(board)
    new_board[row][column] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][i] is EMPTY:
            continue
        if board[i][0] == board[i][1] and board[i][0] == board[i][2]:
            return board[i][0]
        if board[0][i] == board[1][i] and board[0][i] == board[2][i]:
            return board[0][i]
    if board[1][1] is EMPTY:
        return None
    if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return True if winner(board) is not None or len(actions(board)) == 0 else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_s = winner(board)
    if winner_s == X:
        return 1
    if winner_s == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    action, value = minimax_with_value(board)
    return action


def minimax_with_value(board):
    if terminal(board):
        return None, utility(board)
    next_player = player(board)
    new_boards = {}
    all_actions = actions(board)
    if len(all_actions) == 1:
        remaining_action = all_actions.pop()
        return remaining_action, utility(result(board, remaining_action))
    for action in all_actions:
        new_board = result(board, action)
        if winner(new_board) == next_player:
            return action, utility(new_board)
        new_boards[action] = new_board
    next_actions = [(action, minimax_with_value(new_board)[1])
                    for (action, new_board) in new_boards.items()]
    next_values = [next_action[1] for next_action in next_actions]
    if next_player == X:
        goal_value = max(next_values)
    else:
        goal_value = min(next_values)
    outcomes = [next_action[0] for next_action in next_actions if next_action[1] == goal_value]
    return outcomes[0], goal_value
