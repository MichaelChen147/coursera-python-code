"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    Function that takes the current take of the board and
    completes a game, randomly, before returning the result
    """
    emptysquares = board.get_empty_squares()
    random.shuffle(emptysquares)
    for item in emptysquares:
        board.move(item[0], item[1], player)
        player = provided.switch_player(player)
        if board.check_win() != None:
            return

def mc_update_scores(scores, board, player):
    """
    Function that takes a completed board and scores each
    square, based on whether the move resulted in a win or loss
    """
    if board.check_win() == player:
        scorevalue1 = 1
        scorevalue2 = - 1
    elif board.check_win() == provided.switch_player(player):
        scorevalue1 = -1
        scorevalue2 = 1
    else:
        return
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                scores[row][col] += scorevalue1
            elif board.square(row, col) == provided.switch_player(player):
                scores[row][col] += scorevalue2

def get_best_move(board, scores):
    """
    Function that first creates a list of all of the highest
    scoring empty squares, and their associated coordinates,
    and then proceeds to randomly choose one of those sets
    of coordinates as the computer players next move
    """
    empty_squares = board.get_empty_squares()
    possible_moves = []
    for item in empty_squares:
        value = scores[item[0]][item[1]]
        possible_moves.append([value, item[0], item[1]])
    possible_moves.sort(reverse=True)
    best_score = possible_moves[0][0]
    best_moves = [(possible_moves[0][1], possible_moves[0][2])]
    
    for index in range(1, len(possible_moves)):
        if possible_moves[index][0] == best_score:
            best_moves.append((possible_moves[index][1], possible_moves[index][2]))
    choice = random.choice(best_moves)
    return choice   

def mc_move(board, player, trials): 
    """
    The main move function, calls the other functions inside.
    The function loops for NTRIALS number of times, functioning
    as a Monte Carlo testing system to determine a sound game 
    strategy for the computer player.
    """
    score_list = []
    for row in range(board.get_dim()):
        score_row = []
        row = row
        for col in range(board.get_dim()):
            col = col
            score_row.append(0)
        score_list.append(score_row)
    
    for index in range(trials):
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(score_list, board_clone, player)
        index = index
     
    
    best_move = get_best_move(board, score_list)
    return best_move
        
    
                
                
# Test suite for individual functions
#import user34_Uc9ea2tRiN_0 as test_ttt
#test_ttt.test_trial(mc_trial)
#test_ttt.test_update_scores(mc_update_scores, MCMATCH, MCOTHER)
#print
# test_ttt.test_update_scores(mc_update_scores, MCMATCH, MCOTHER)
# print
#test_ttt.test_best_move(get_best_move)

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
