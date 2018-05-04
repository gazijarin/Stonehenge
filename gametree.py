"""
Class GameTree module for iterative minimax.
"""
from typing import List, Union, Any


class GameTree:
    """
    A GameTree ADT that identifies the root with the entire tree.

    === Attributes ===
    state - initial game state (root node)
    score - score of the state
    move - move that caused the state
    children - subsequent game states (child nodes)
    """
    state: Any
    score: int
    move: Any
    children: Union[List["GameTree"], None]

    def __init__(self, state: Any = None,
                 score: int = None,
                 move: Any = None,
                 children: Union[List["GameTree"], None] = None) -> None:
        """
        Create GameTree self with content state, score, move and 0 or more
        children.
        """

        self.state = state
        # copy children if not None
        self.children = children[:] if children is not None else []
        self.score = score
        self.move = move

