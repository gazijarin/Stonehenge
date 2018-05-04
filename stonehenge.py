"""
The Stonehenge Game and the Stonehenge GameState.
"""
from typing import Any, Dict, List, Union
from game import Game
from game_state import GameState

# HELPER FUNCTION(S)


def modify_board(board: Dict[int, Union[List[str], List[int]]],
                 ley_lines: Dict[int, Union[int, str]],
                 move: str, num: int) -> None:
    """
    Modify board's value to num if it is equal to move. If half of the
    values in the key of board is modified to num, modify the values in that key
    of ley_lines to num.

    Preconditions:
    (1) num should either be 1 or 2
    (2) board and ley_lines should have the same corresponding keys
    """

    for ley_line in board:
        for cell in board[ley_line]:
            if cell == move:
                cell_index = board[ley_line].index(cell)
                board[ley_line][cell_index] = num
    for ley_line in board:
        cells_claimed = 0
        for cell in board[ley_line]:
            if cell == num:
                cells_claimed += 1
        if ((len(board[ley_line]) / 2) <= cells_claimed
                and not str(ley_lines[ley_line]).isdigit()):
            ley_lines[ley_line] = num


# CONSTANTS FOR TESTING

GAMEBOARD_1 = {1: ['A'], 2: ['B', 'C'], 3: ['B'], 4: ['A', 'C'],
               5: ['C'], 6: ['A', 'B']}

GAMEBOARD_1_MAKE_MOVE_A = {1: [1], 2: ['B', 'C'], 3: ['B'], 4: [1, 'C'],
                           5: ['C'], 6: [1, 'B']}

IDEAL_BOARD_STR = \
"""\
      @   @
     /   /
@ - A - B
     \\ / \\
  @ - C   @
       \\
        @"""

IDEAL_BOARD_REPR = \
"""\
      @   @
     /   /
@ - A - B
     \\ / \\
  @ - C   @
       \\
        @
Turn: Player 1"""


class StonehengeState(GameState):
    """
    The current state of Stonehenge game. The Stonehenge state is identified
    by the current player, side length, gameboard, and ley lines.

    == Attributes ==
    (1) p1_turn - whether it is p1's turn or not
    (2) side_length - the board sidelength
    (3) gameboard - a dict representation of cells, organized by the ley_lines
    that hold them (depends on sidelength).
    i.e. ley_lines are numbered clock-wise starting from the first down-right
    diagonal and therefore the last ley_line will always contain the
    cells A and B.
    (4) ley_lines - a dict representation of ley_lines that have the values
    of either '@', 1 or 2.
    """

    p1_turn: bool
    side_length: int
    gameboard: Dict[int, Union[List[str], List[int]]]
    ley_lines: Dict[int, Union[int, str]]

    def __init__(self, is_p1_turn: bool, side_length: int = None,
                 gameboard: Dict[int, Union[List[str], List[int]]] = None,
                 ley_lines: Dict[int, Union[int, str]] = None) -> None:
        """
        Initialize a new StonehengeState.

        >>> s = StonehengeState(True, 1)
        >>> s.p1_turn
        True
        >>> s.side_length
        1
        >>> s.gameboard == GAMEBOARD_1
        True
        >>> s.ley_lines
        {1: '@', 2: '@', 3: '@', 4: '@', 5: '@', 6: '@'}
        """

        # inherit attribute p1_turn from parent class
        GameState.__init__(self, is_p1_turn)

        if side_length is None:  # prompt if sidelength is not entered
            side_length = int(input("Enter the side-length of "
                                    "the board: "))
        self.side_length = side_length

        # set gameboard to a fixed representation depending on self.side_length
        # if gameboard is not entered.
        if self.side_length == 1 and gameboard is None:
            gameboard = {1: ['A'], 2: ['B', 'C'], 3: ['B'], 4: ['A', 'C'],
                         5: ['C'], 6: ['A', 'B']}
        elif self.side_length == 2 and gameboard is None:
            gameboard = {1: ['A', 'C'], 2: ['B', 'D', 'F'], 3: ['E', 'G'],
                         4: ['B', 'E'], 5: ['A', 'D', 'G'], 6: ['C', 'F'],
                         7: ['F', 'G'], 8: ['C', 'D', 'E'], 9: ['A', 'B']}
        elif self.side_length == 3 and gameboard is None:
            gameboard = {1: ['A', 'C', 'F'], 2: ['B', 'D', 'G', 'J'],
                         3: ['E', 'H', 'K'], 4: ['I', 'L'], 5: ['B', 'E', 'I'],
                         6: ['A', 'D', 'H', 'L'], 7: ['C', 'G', 'K'],
                         8: ['F', 'J'], 9: ['J', 'K', 'L'],
                         10: ['F', 'G', 'H', 'I'], 11: ['C', 'D', 'E'],
                         12: ['A', 'B']}
        elif self.side_length == 4 and gameboard is None:
            gameboard = {1: ['A', 'C', 'F', 'J'], 2: ['B', 'D', 'G', 'K', 'O'],
                         3: ['E', 'H', 'L', 'P'], 4: ['T', 'M', 'Q'],
                         5: ['N', 'R'], 6: ['B', 'E', 'T', 'N'],
                         7: ['A', 'D', 'H', 'M', 'R'], 8: ['C', 'G', 'L', 'Q'],
                         9: ['F', 'K', 'P'], 10: ['J', '0'],
                         11: ['O', 'P', 'Q', 'R'],
                         12: ['J', 'K', 'L', 'M', 'N'],
                         13: ['F', 'G', 'H', 'I'], 14: ['C', 'D', 'E'],
                         15: ['A', 'B']}
        elif self.side_length == 5 and gameboard is None:
            gameboard = {1: ['A', 'C', 'F', 'J', 'O'],
                         2: ['B', 'D', 'G', 'K', 'P', 'U'],
                         3: ['E', 'H', 'L', 'Q', 'V'], 4: ['I', 'M', 'R', 'W'],
                         5: ['N', 'S', 'X'], 6: ['T', 'Y'],
                         7: ['B', 'E', 'I', 'N', 'T'],
                         8: ['A', 'D', 'H', 'M', 'S', 'Y'],
                         9: ['C', 'G', 'L', 'R', 'X'], 10: ['F', 'K', 'Q', 'W'],
                         11: ['J', 'P', 'V'], 12: ['O', 'U'],
                         13: ['U', 'V', 'W', 'X', 'Y'],
                         14: ['O', 'P', 'Q', 'R', 'S', 'T'],
                         15: ['J', 'K', 'L', 'M', 'N'],
                         16: ['F', 'G', 'H', 'I'], 17: ['C', 'D', 'E'],
                         18: ['A', 'B']}
        self.gameboard = gameboard

        # create a new ley_lines dict if ley_lines is not entered.
        # set the dict's keys corresponding to self.gameboard's ley-lines.
        if ley_lines is None:
            ley_lines = {}
            for ley_line in self.gameboard:
                ley_lines[ley_line] = '@'
        self.ley_lines = ley_lines

    def __str__(self) -> str:
        """
        Return a string representation of the current state of Stonehenge.

        >>> s = StonehengeState(True, 1)
        >>> str(s) == IDEAL_BOARD_STR
        True
        """

        gameboard = ''

        # set gameboard to one of five layouts depending on self.side_length
        if self.side_length == 1:
            gameboard += \
                '      {0}   {1}\n' \
                '     /   /\n' \
                '{2} - {3} - ' \
                '{4}\n' \
                '     \\ / \\\n' \
                '  {5} - {6}   ' \
                '{7}\n' \
                '       \\\n' \
                '        {8}'.format(self.ley_lines[1],
                                     self.ley_lines[2],
                                     self.ley_lines[6],
                                     self.gameboard[1][0],
                                     self.gameboard[2][0],
                                     self.ley_lines[5],
                                     self.gameboard[2][1],
                                     self.ley_lines[3],
                                     self.ley_lines[4])
        elif self.side_length == 2:
            gameboard += \
                '        {0}   {1}\n' \
                '       /   /\n' \
                '  {2} - {3} - ' \
                '{4}   {5}\n' \
                '     / \\ / \\ /\n' \
                '{6} - {7} - ' \
                '{8} - {9}\n' \
                '     \\ / \\ / \\\n' \
                '  {10} - {11} - ' \
                '{12}   {13}\n' \
                '       \\   \\\n' \
                '        {14}   {15}'.format(self.ley_lines[1],
                                             self.ley_lines[2],
                                             self.ley_lines[9],
                                             self.gameboard[1][0],
                                             self.gameboard[2][0],
                                             self.ley_lines[3],
                                             self.ley_lines[8],
                                             self.gameboard[1][1],
                                             self.gameboard[2][1],
                                             self.gameboard[3][0],
                                             self.ley_lines[7],
                                             self.gameboard[7][0],
                                             self.gameboard[7][1],
                                             self.ley_lines[4],
                                             self.ley_lines[6],
                                             self.ley_lines[5])
        elif self.side_length == 3:
            gameboard += \
                '          {0}   {1}\n' \
                '         /   /\n' \
                "    {2} - {3} - " \
                "{4}   {5}\n" \
                "       / \\ / \\ /\n" \
                "  {6} - {7} - " \
                "{8} - {9}   " \
                "{10}\n" \
                "     / \\ / \\ / \\ /\n" \
                "{11} - {12} - " \
                "{13} - {14} - " \
                "{15}\n" \
                "     \\ / \\ / \\ / \\\n" \
                "  {16} - {17} - " \
                "{18} - {19}   " \
                "{20}\n" \
                "       \\   \\   \\\n" \
                "        {21}   {22}   " \
                "{23}".format(self.ley_lines[1],
                              self.ley_lines[2],
                              self.ley_lines[12],
                              self.gameboard[1][0],
                              self.gameboard[2][0],
                              self.ley_lines[3],
                              self.ley_lines[11],
                              self.gameboard[1][1],
                              self.gameboard[2][1],
                              self.gameboard[3][0],
                              self.ley_lines[4],
                              self.ley_lines[10],
                              self.gameboard[10][0],
                              self.gameboard[10][1],
                              self.gameboard[10][2],
                              self.gameboard[10][3],
                              self.ley_lines[9],
                              self.gameboard[9][0],
                              self.gameboard[9][1],
                              self.gameboard[9][2],
                              self.ley_lines[5],
                              self.ley_lines[8],
                              self.ley_lines[7],
                              self.ley_lines[6])
        elif self.side_length == 4:
            gameboard += \
                '            {0}   {1}\n' \
                '           /   /\n' \
                '      {2} - {3} - ' \
                '{4}   {5}\n' \
                '         / \\ / \\ /\n' \
                '    {6} - {7} -' \
                ' {8} - {9}   ' \
                '{10}\n' \
                '       / \\ / \\ / \\ /\n' \
                '  {11} - {12} - ' \
                '{13} - {14} - ' \
                '{15}   {16}\n' \
                '     / \\ / \\ / \\ / \\ /\n' \
                '{17} - {18} - ' \
                '{19} - {20} -' \
                ' {21} - {22}\n' \
                '     \\ / \\ / \\ / \\ / \\\n' \
                '  {23} - {24} - ' \
                '{25} - {26} - ' \
                '{27}   {28}\n' \
                '       \\   \\   \\   \\\n' \
                '        {29}   {30}   ' \
                '{31}   {32}'.format(self.ley_lines[1],
                                     self.ley_lines[2],
                                     self.ley_lines[15],
                                     self.gameboard[1][0],
                                     self.gameboard[2][0],
                                     self.ley_lines[3],
                                     self.ley_lines[14],
                                     self.gameboard[1][1],
                                     self.gameboard[2][1],
                                     self.gameboard[3][0],
                                     self.ley_lines[4],
                                     self.ley_lines[13],
                                     self.gameboard[13][0],
                                     self.gameboard[13][1],
                                     self.gameboard[13][2],
                                     self.gameboard[13][3],
                                     self.ley_lines[5],
                                     self.ley_lines[12],
                                     self.gameboard[12][0],
                                     self.gameboard[12][1],
                                     self.gameboard[12][2],
                                     self.gameboard[12][3],
                                     self.gameboard[12][4],
                                     self.ley_lines[11],
                                     self.gameboard[11][0],
                                     self.gameboard[11][1],
                                     self.gameboard[11][2],
                                     self.gameboard[11][3],
                                     self.ley_lines[6],
                                     self.ley_lines[10],
                                     self.ley_lines[9],
                                     self.ley_lines[8],
                                     self.ley_lines[7])
        elif self.side_length == 5:
            gameboard += \
                '              {0}   {1}\n' \
                '             /   /\n' \
                '        {2} - {3} - ' \
                '{4}   {5}\n' \
                '           / \\ / \\ /\n' \
                '      {6} - {7} - ' \
                '{8} - {9}   ' \
                '{10}\n' \
                '         / \\ / \\ / \\ /\n' \
                '    {11} - {12} - ' \
                '{13} - {14} - ' \
                '{15}   {16}\n' \
                '       / \\ / \\ / \\ / \\ /\n' \
                '  {17} - {18} - ' \
                '{19} - {20} - ' \
                '{21} - {22}   ' \
                '{23}\n' \
                '     / \\ / \\ / \\ / \\ / \\ /\n' \
                '{24} - {25} - ' \
                '{26} - {27} - ' \
                '{28} - {29} - ' \
                '{30}\n' \
                '     \\ / \\ / \\ / \\ / \\ / \\\n' \
                '  {31} - {32} - ' \
                '{33} - {34} - ' \
                '{35} - {36}   ' \
                '{37}\n' \
                '       \\   \\   \\   \\   \\\n' \
                '        {38}   {39}   ' \
                '{40}   {41}   ' \
                '{42}'.format(self.ley_lines[1],
                              self.ley_lines[2],
                              self.ley_lines[18],
                              self.gameboard[1][0],
                              self.gameboard[2][0],
                              self.ley_lines[3],
                              self.ley_lines[17],
                              self.gameboard[17][0],
                              self.gameboard[17][1],
                              self.gameboard[17][2],
                              self.ley_lines[4],
                              self.ley_lines[16],
                              self.gameboard[16][0],
                              self.gameboard[16][1],
                              self.gameboard[16][2],
                              self.gameboard[16][3],
                              self.ley_lines[5],
                              self.ley_lines[15],
                              self.gameboard[15][0],
                              self.gameboard[15][1],
                              self.gameboard[15][2],
                              self.gameboard[15][3],
                              self.gameboard[15][4],
                              self.ley_lines[6],
                              self.ley_lines[14],
                              self.gameboard[14][0],
                              self.gameboard[14][1],
                              self.gameboard[14][2],
                              self.gameboard[14][3],
                              self.gameboard[14][4],
                              self.gameboard[14][5],
                              self.ley_lines[13],
                              self.gameboard[13][0],
                              self.gameboard[13][1],
                              self.gameboard[13][2],
                              self.gameboard[13][3],
                              self.gameboard[13][4],
                              self.ley_lines[7],
                              self.ley_lines[12],
                              self.ley_lines[11],
                              self.ley_lines[10],
                              self.ley_lines[9],
                              self.ley_lines[8])
        else:
            assert "Make sure the side_length is in range [1, 5]."

        return gameboard

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this Stonehenge state.

        >>> s = StonehengeState(True, 1)
        >>> s.get_possible_moves()
        ['A', 'B', 'C']
        >>> s.make_move('A').get_possible_moves()
        []
        """

        possible_moves = []  # initially create an empty list of possible moves

        p1_claimed = 0  # initially set the ley_lines p1 claimed to 0
        p2_claimed = 0  # initially set the ley_lines p2 claimed to 0

        # count the ley lines captured by both p1 and p2 given self.ley_lines
        for ley_line in self.ley_lines:
            if self.ley_lines[ley_line] == 1:
                p1_claimed += 1
            elif self.ley_lines[ley_line] == 2:
                p2_claimed += 1
            else:
                pass

        # compare the amount captured to half the length of self.ley_lines
        # if it is at least half the length, then return an empty list
        if ((len(self.ley_lines) / 2) <= p1_claimed
                or (len(self.ley_lines) / 2) <= p2_claimed):
            return possible_moves

        # iterate through the gameboard and add them to possible_moves
        # if they are unclaimed (still capital letters) and if they
        # are not already in possible_moves.
        for ley_line in self.gameboard:
            for cell in self.gameboard[ley_line]:
                if not str(cell).isdigit() and cell not in possible_moves:
                    possible_moves.append(cell)
                else:
                    pass

        possible_moves.sort()  # sort in alphabetical order
        return possible_moves

    def make_move(self, move: Any) -> 'StonehengeState':
        """
        Return the StonehengeState that results from applying move to this
        StonehengeState.

        >>> s = StonehengeState(True, 1)
        >>> print(s.make_move('A').ley_lines)
        {1: 1, 2: '@', 3: '@', 4: 1, 5: '@', 6: 1}
        >>> s.make_move('A').gameboard == GAMEBOARD_1_MAKE_MOVE_A
        True
        >>> print(s.ley_lines)
        {1: '@', 2: '@', 3: '@', 4: '@', 5: '@', 6: '@'}
        >>> s.gameboard == GAMEBOARD_1
        True
        """

        new_ley_lines = self.ley_lines.copy()  # make a copy of self.ley_lines
        new_state = ''  # assign new_state to a dummy empty string
        new_board = {}  # create a new gameboard

        # accumulate the new gameboard by copying the contents of self.gameboard
        for ley_line in self.gameboard:
            new_board[ley_line] = self.gameboard[ley_line][:]

        # use helper function modify_board to change the values of cells and
        # ley_lines depending on the move
        # re-assign new_state to the next StonehengeState after move is made
        if self.get_current_player_name() == 'p1':
            modify_board(new_board, new_ley_lines, move, 1)
            new_state = StonehengeState(False, self.side_length,
                                        new_board, new_ley_lines)
        elif self.get_current_player_name() == 'p2':
            modify_board(new_board, new_ley_lines, move, 2)
            new_state = StonehengeState(True, self.side_length,
                                        new_board, new_ley_lines)

        return new_state

    def __repr__(self) -> Any:
        """
        Return a representation of this StonehengeState (which can be used for
        equality testing).

        >>> s = StonehengeState(True, 1)
        >>> repr(s) == IDEAL_BOARD_REPR
        True
        """

        representation = self.__str__()
        # add current player to the string representation
        if self.p1_turn:
            representation += '\nTurn: Player 1'
        elif not self.p1_turn:
            representation += '\nTurn: Player 2'

        return representation

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from StongehengeState self.

        >>> s = StonehengeState(True, 1)
        >>> s.rough_outcome()
        1
        """

        # return a LOSE (-1) if current player lost at the start of game
        if self.get_possible_moves() == []:
            return self.LOSE

        other_player_record = []  # keep track of other player's wins/losses

        for move in self.get_possible_moves():
            first_state = self.make_move(move)

            # return a WIN (1) if current player wins by applying a move
            if first_state.get_possible_moves() == []:
                return self.WIN

            # set other_player_can_win to False initially
            other_player_can_win = False
            for other_move in first_state.get_possible_moves():
                second_state = first_state.make_move(other_move)

                # re-set other_player_can_win to True iff the other player
                # wins by the next move
                if second_state.get_possible_moves() == []:
                    other_player_can_win = True
            # collect all the times other player has won or lost
            other_player_record.append(other_player_can_win)

        # return a LOSE (-1) iff the other player has a chance of winning
        # for every move next state
        if all([True in other_player_record]):
            return self.LOSE
        # else, return a DRAW (0)
        return self.DRAW


class Stonehenge(Game):
    """
    A Stonehenge game. Each Stonehenge game is identified by its current
    player's turn and its current state.

    == Attributes ==
    (1) p1_starts - player one begins the game if True; else, player two does
    (2) current_state - the current state of Stonehenge game
    """
    p1_starts: bool
    current_state: StonehengeState

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Stonehenge game, using p1_starts to find who the first
        player is.
        """

        self.p1_starts = p1_starts

        if p1_starts:
            self.current_state = StonehengeState(True)
        elif not p1_starts:
            self.current_state = StonehengeState(False)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Stonehenge game.
        """

        instructions = "Players take turns claiming cells. " + \
            "When a player captures at least half of the cells " + \
            "in the ley-line, then the player captures that ley-line. " + \
            "The first player to capture at least half of the ley-lines " + \
            "is the winner."

        return instructions

    def is_over(self, state: "StonehengeState") -> bool:
        """
        Return whether or not this Stonehenge game is over at state.
        """

        p1_claimed = 0  # initially set the ley_lines p1 claimed to 0
        p2_claimed = 0  # initially set the ley_lines p2 claimed to 0

        # count the ley lines captured by both p1 and p2 given self.ley_lines
        for ley_line in state.ley_lines:
            if state.ley_lines[ley_line] == 1:
                p1_claimed += 1
            elif state.ley_lines[ley_line] == 2:
                p2_claimed += 1
            else:
                pass

        # return True iff at least half of the ley-lines have been claimed
        return ((len(state.ley_lines) / 2) <= p1_claimed
                or (len(state.ley_lines) / 2)
                <= p2_claimed)

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the Stonehenge game.

        Precondition: player is 'p1' or 'p2'.
        """

        p1_claimed = 0  # initially set the ley_lines p1 claimed to 0
        p2_claimed = 0  # initially set the ley_lines p2 claimed to 0

        # count the ley lines captured by both p1 and p2 given self.ley_lines
        for ley_line in self.current_state.ley_lines:
            if self.current_state.ley_lines[ley_line] == 1:
                p1_claimed += 1
            elif self.current_state.ley_lines[ley_line] == 2:
                p2_claimed += 1

        # return True iff player claims at least half of the ley-lines
        if player == 'p1':
            return (len(self.current_state.ley_lines) / 2) <= p1_claimed
        elif player == 'p2':
            return (len(self.current_state.ley_lines) / 2) <= p2_claimed
        return False

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """

        if string.upper() in self.current_state.get_possible_moves():
            return string.upper()
        return -1
