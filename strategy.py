"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, Union
from game import Game
from game_state import GameState
from gametree import GameTree


def interactive_strategy(game: Any) -> Union[str, int]:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Union[str, int]:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def recursive_state(game: Game, current_state: GameState) -> int:
    """
    Return the highest guaranteed score recursively given a game and its
    current_state.
    """

    scores = []  # create a list to collect the player's scores for each move
    state_scores = []  # create a list to collect the resultant state scores
    old_state = game.current_state

    if game.is_over(current_state):  # check if game state is over
        current_player = current_state.get_current_player_name()
        # set current_player and other_player to either 'p1' or 'p2'
        if current_player == 'p1':
            other_player = 'p2'
        else:
            other_player = 'p1'
        game.current_state = current_state
        # return -1 if the current player of that state won
        if game.is_winner(current_state.get_current_player_name()):
            game.current_state = old_state
            return 1
        # return 1 if the current player of that state lost
        elif game.is_winner(other_player):
            game.current_state = old_state
            return -1
        # else, return 0 for a tie.
        game.current_state = old_state
        return 0
    else:
        # if game state is not over, access the new state for each
        # move available.
        # append the score returned and multiply it by -1, since the
        # current_player of that state is the other_player for
        # our original state. (zero-sum game)
        for move in current_state.get_possible_moves():
            new_state = current_state.make_move(move)
            scores.append(-1 * recursive_state(game, new_state))

    game.current_state = old_state
    state_scores.append(max(scores))  # get the highest guaranteed score
    return max(state_scores)  # return the highest guaranteed outcome


def recursive_minimax_strategy(game: Game) -> Any:
    """
    Return a move for game that yields the "highest guaranteed score"
    recursively for each step for current player.
    """

    moves = {}  # a dict to record the moves corresponding to different outcomes
    old_state = game.current_state

    for move in game.current_state.get_possible_moves():
        current_player = game.current_state.get_current_player_name()
        # set current_player and other_player to either 'p1' or 'p2'
        if current_player == 'p1':
            other_player = 'p2'
        else:
            other_player = 'p1'
        # access the new_state attained from each possible move
        new_state = game.current_state.make_move(move)
        if game.is_over(new_state):  # check if state is over
            game.current_state = new_state
            # record move as key and 1 as value
            # if the current_player of that state won
            if game.is_winner(current_player):
                game.current_state = old_state
                moves[move] = 1
            # record -1 as value to moves for the move
            # if other_player won
            elif game.is_winner(other_player):
                game.current_state = old_state
                moves[move] = -1
            # else, record 0 to moves for the move.
            else:
                game.current_state = old_state
                moves[move] = 0
        else:
            # if state is not over, check the next states.
            # multiply by -1 because of the game's zero-sum rule.
            moves[move] = -1 * recursive_state(game, new_state)

    game.current_state = old_state
    # return the move that guarantees a win for the current_player
    for move in moves:
        if moves[move] == 1:
            return move
    # if not, return the move that guarantees a tie for the current_player
    for move in moves:
        if moves[move] == 0:
            return move
    # else, return the last resort.
    for move in moves:
        if moves[move] == -1:
            return move
    return None


def iterative_minimax_strategy(game: Game) -> Any:
    """
    Return a move for game that yields the "highest guaranteed score"
    iteratively for each step for current player.
    """

    # create an empty list for holding game-trees
    game_stack = []
    # store the game's current_state in a GameTree
    initial_game_tree = GameTree(game.current_state)
    # append the GameTree to the game_stack
    game_stack.append(initial_game_tree)
    # store game's current_state in old_state
    old_state = game.current_state

    while game_stack != []:
        game_tree = game_stack.pop()  # pop the last GameTree appended
        game_state = game_tree.state
        current_player = game_state.get_current_player_name()
        # set current_player and other_player to either 'p1' or 'p2'
        if current_player == 'p1':
            other_player = 'p2'
        else:
            other_player = 'p1'
        if game.is_over(game_state):  # check if state is over
            game.current_state = game_state
            # set the node's score to 1 if current_player won
            if game.is_winner(current_player):
                game.current_state = old_state
                game_tree.score = 1
            # set the node's score to -1 if other_player won
            elif game.is_winner(other_player):
                game.current_state = old_state
                game_tree.score = -1
            # else, set the node's score to 0 for a tie
            else:
                game.current_state = old_state
                game_tree.score = 0
        # if we haven't looked at the game_tree yet,
        elif not game_tree.children:
            game_tree.children = []
            # access the new_states and append them as children
            for move in game_tree.state.get_possible_moves():
                new_state = game_tree.state.make_move(move)
                child = GameTree(state=new_state, move=move)
                game_tree.children.append(child)
            # append the ga-me_tree and its children into game_stack
            game_stack.append(game_tree)
            for child in game_tree.children:
                game_stack.append(child)
        # if we did visit the node before...
        elif game_tree.children:
            child_scores = []  # create a child_scores list to store scores
            for child in game_tree.children:
                # append the opposite of the score (zero-sum rule)
                child_scores.append(-1 * child.score)
            # set the highest guaranteed score to the state
            game_tree.score = max(child_scores)

    # loop through the states reachable by the initial_game_tree
    # since the child scores are still for the other_player, we multiply
    # them by -1.
    for child in initial_game_tree.children:
        # look for the child with the highest guaranteed score
        if child.score == -1:
            # return the corresponding move that guarantees a win
            return child.move
    # if not, return the move that guarantees a tie for the current_player
    for child in initial_game_tree.children:
        if child.score == 0:
            return child.move
    # else, return the last resort.
    for child in initial_game_tree.children:
        if child.score == 1:
            return child.move
    return None
