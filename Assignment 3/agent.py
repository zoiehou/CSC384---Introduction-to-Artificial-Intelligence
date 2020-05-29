"""
An AI player for Othello.
#Dark = 1; Light = 2
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

seen_states = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    scores = get_score(board)
    if color == 1:
        score_final = scores[0] - scores[1]
    elif color == 2:
        score_final = scores[1] - scores[0]
    return score_final

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT
    #Dark = 1; Light = 2
    if caching != 0:
        if seen_states[str(board)] != 0:
            return seen_states[str(board)]

    min_utility = float('inf')
    min_move = (-1, -1)

    if color == 1:
        new_color = 2
    elif color == 2:
        new_color = 1

    legal = get_possible_moves(board, new_color)

    if limit == 0 or len(legal) == 0:
        min_utility = compute_utility(board, color)
        seen_states[str(board)] = (min_move, min_utility)
        return (min_move, min_utility)

    else:
        for move in legal:
            played_board = play_move(board, new_color, move[0], move[1])
            played_move, played_utility = minimax_max_node(played_board, color, limit-1, caching)
            if played_utility < min_utility:
                min_utility = played_utility
                min_move = move
        seen_states[str(board)] = (min_move, min_utility)
        return (min_move, min_utility)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT
    #Dark = 1; Light = 2
    if caching != 0:
        if seen_states[str(board)] != 0:
            return seen_states[str(board)]

    max_utility = float('-inf')
    max_move = (-1, -1)
    legal = get_possible_moves(board, color)

    if limit == 0 or len(legal) == 0:
        max_utility = compute_utility(board, color)
        seen_states[str(board)] = (max_move, max_utility)
        return (max_move, max_utility)

    else:
        for move in legal:
            played_board = play_move(board, color, move[0], move[1])
            played_move, played_utility = minimax_min_node(played_board, color, limit-1, caching)
            if played_utility > max_utility:
                max_utility = played_utility
                max_move = move
        seen_states[str(board)] = (max_move, max_utility)
        return (max_move, max_utility)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT
    selected_move, selected_utility = minimax_max_node(board, color, limit, caching)
    return selected_move

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    #Dark = 1; Light = 2
    if caching != 0:
        if seen_states[str(board)] != 0:
            return seen_states[str(board)]

    min_utility = float('inf')
    min_move = (-1, -1)

    if color == 1:
        new_color = 2
    elif color == 2:
        new_color = 1

    legal = get_possible_moves(board, new_color)

    if limit == 0 or len(legal) == 0:
        min_utility = compute_utility(board, color)
        seen_states[str(board)] = (min_move, min_utility)
        return (min_move, min_utility)

    else:
        if ordering != 0:
            order = []
            for order_move in legal:
                order_board = play_move(board, new_color, order_move[0], order_move[1])
                order_utility = compute_utility(order_board, color)
                order.append((order_move, order_utility))
            order.sort(key=lambda tuples: tuples[1], reverse = False)
            legal = [tup[0] for tup in order]
        for move in legal:
            played_board = play_move(board, new_color, move[0], move[1])
            played_m, played_u = alphabeta_max_node(played_board, color, alpha, beta, limit-1, caching, ordering)
            if played_u < min_utility:
                min_utility = played_u
                min_move = move
            if min_utility <= alpha:
                seen_states[str(board)] = (min_move, min_utility)
                return (min_move, min_utility)
            beta = min(beta, min_utility)
        seen_states[str(board)] = (min_move, min_utility)
        return (min_move, min_utility)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    #Dark = 1; Light = 2
    if caching != 0:
        if seen_states[str(board)] != 0:
            return seen_states[str(board)]

    max_utility = float('-inf')
    max_move = (-1, -1)

    legal = get_possible_moves(board, color)

    if limit == 0 or len(legal) == 0:
        max_utility = compute_utility(board, color)
        seen_states[str(board)] = (max_move, max_utility)
        return (max_move, max_utility)

    else:
        if ordering != 0:
            order = []
            for order_move in legal:
                order_board = play_move(board, color, order_move[0], order_move[1])
                order_utility = compute_utility(order_board, color)
                order.append((order_move, order_utility))
            order.sort(key=lambda tuples: tuples[1], reverse=True)
            legal = [tup[0] for tup in order]
        for move in legal:
            played_board = play_move(board, color, move[0], move[1])
            played_m, played_u = alphabeta_min_node(played_board, color, alpha, beta, limit - 1, caching, ordering)
            if played_u > max_utility:
                max_utility = played_u
                max_move = move
            if max_utility >= beta:
                seen_states[str(board)] = (max_move, max_utility)
                return (max_move, max_utility)
            alpha = max(alpha, max_utility)
        seen_states[str(board)] = (max_move, max_utility)
        return (max_move, max_utility)

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT
    a = float('-inf')
    b = float('inf')
    selected_move, selected_utility = alphabeta_max_node(board, color, a, b, limit, caching, ordering)
    return selected_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
