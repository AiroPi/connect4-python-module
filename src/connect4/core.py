from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal, Sequence, TypeAlias, cast

from connect4.errors import ColumnFull, GameOver, InvalidColumn

Token: TypeAlias = str


class Players(Enum):
    NONE = 0
    ONE = 1
    TWO = 2


class Connect4:
    """
    Class to play connect 4. Use function play to play. Player switch automatically.
    """

    def __init__(self, dimensions: Sequence[int] = (7, 6)) -> None:
        """Setup the game.

        Args:
            dimensions (Sequence[int], optional): The dimensions of the game (columns, rows). Defaults to (7, 6).
        """
        self._dimensions: tuple[int, int] = (dimensions[0], dimensions[1])
        self._idim: tuple[int, int] = (self._dimensions[0] - 1, self._dimensions[1] - 1)
        self.plays_history: list[tuple[int, int]] = []
        self._win_points: set[tuple[int, int]] = set()

        self._board: list[list[Players]] = self.create_empty_board(self._dimensions)
        self._turn: Players = Players.ONE

        self._dim = self._dimensions

    @property
    def dimensions(self) -> tuple[int, int]:
        """Get the board dimensions.

        Returns:
            tuple[int, int]: A tuple with the board dimensions. (columns, rows)
        """
        return self._dimensions

    @property
    def yxboard(self) -> list[list[Players]]:
        """Return the board, but the sub lists are the columns.

        Returns:
            list[list[Players]]: The board as an array. The columns are the sub lists. (0: empty, 1: player 1, 2: player 2)
        """
        return [[row[i] for row in self._board] for i in range(self._dim[1])[::-1]]

    @property
    def board(self) -> list[list[Players]]:
        """Get the current board.

        Returns:
            list[list[Players]]: The board as an array. The rows are the sub lists (consider yxboard for the inverse). (0: empty, 1: player 1, 2: player 2)
        """
        return self._board

    @property
    def is_over(self) -> bool:
        """Check if the game is over.

        Returns:
            bool: True if the game is over.
        """
        return bool(self._win_points)

    @property
    def winner(self) -> Players | None:
        """Get the winner. None if no winner. Players.NONE if tie.

        Returns:
            Players: The winner.
        """
        if self._win_points or self.turn == Players.NONE:
            return self.turn
        return None

    @property
    def turn(self) -> Players:
        """Get the current player.

        Returns:
            Players: The player turn. Players.NONE if it's a tie.
        """
        return self._turn

    @turn.setter
    def turn(self, turn: Players) -> None:
        """Set player turn (not recommended).

        Args:
            turn (Literal[Players.ONE, Players.TWO, 1, 2]): The player turn.
        """
        if turn == Players.ONE or turn == 1:
            self._turn = Players.ONE
        elif turn == Players.TWO or turn == 2:
            self._turn = Players.TWO
        elif turn == Players.NONE or turn == 0:
            self._turn = Players.NONE
        else:
            raise ValueError("Invalid player turn")

    @staticmethod
    def create_empty_board(dimensions: Sequence[int]) -> list[list[Players]]:
        """Create a 0 filled board.

        Args:
            dimensions (Sequence[int]): Dimensions to use for the board.

        Returns:
            list[list[Players]]: A 0 filled board.
        """
        return [[Players.NONE] * dimensions[0] for _ in range(dimensions[1])]

    def strboard(self, player1: Token = "x", player2: Token = "o", win_player1: Token = "X", win_player2: Token = "O", empty: Token = " ") -> str:
        """Format the board into a string.

        Args:
            player1 (Token, optional): The symbol to use for player 1. Defaults to "x".
            player2 (Token, optional): The symbol to use for player 2. Defaults to "o".
            win_player1 (Token, optional): The symbol to use to highlight the player 1 win. Defaults to "X".
            win_player2 (Token, optional): The symbol to use to highlight the player 2 win. Defaults to "O".
            empty (Token, optional): The symbol to use for empty slots. Defaults to " ".

        Returns:
            str: The string board.
        """
        board: list[list[int]] = [[case.value for case in row] for row in self.board]
        for row, column in self._win_points:
            board[row][column] = 3 if self._board[row][column] == Players.ONE else 4
        return ''.join(''.join((empty, player1, player2, win_player1, win_player2)[case] for case in row) + '\n' for row in board)[:-1]

    def play(self, column: int) -> set[tuple[int, int]]:
        """Drop a token in a column. Column is index based (starts at 0).

        Args:
            column (int): The column to drop the token. (First column is 0)

        Raises:
            GameOver: If the game is over.
            InvalidColumn: If the column is invalid. (Out of range)
            ColumnFull: If the column is full.

        Returns:
            set[tuple[int, int]]: The points that's do the player win, if any.
        """
        if self._win_points or self.turn == Players.NONE:
            raise GameOver(self.turn)

        if column < 0 or column >= self._dim[0]:
            raise InvalidColumn(column)

        for i, row in enumerate(self._board[::-1]):
            if row[column] == Players.NONE:
                row[column] = self.turn
                break
        else:
            raise ColumnFull(column)

        self.plays_history.append((column, self._idim[1] - i))
        self._get_win(column, self._idim[1] - i)

        if not self._win_points:
            if self._check_tie():
                self.turn = Players.NONE
            elif self.turn == Players.ONE:
                self.turn = Players.TWO
            else:
                self.turn = Players.ONE

        return self._win_points

    def _get_win(self, icolumn: int, irow: int) -> None:
        """Check if the player won, and if so, add the points to the win_points set.

        Args:
            icolumn (int): The index-based column of the last play.
            irow (int): The index-based row of the last play.
        """

        target = self.turn

        @dataclass
        class T:
            positions: set
            before: bool
            after: bool

            def __bool__(self) -> bool:
                return self.before or self.after

        lines: dict[str, T] = {
            'horizontal': T({(irow, icolumn)}, True, True),
            'vertical': T({(irow, icolumn)}, False, True),
            'diagonal1': T({(irow, icolumn)}, True, True),
            'diagonal2': T({(irow, icolumn)}, True, True)
        }

        for k in range(1, max(self._dim[0], self._dim[1])):
            line = lines['horizontal']
            if line.before and (i := icolumn - k) >= 0 and self._board[irow][i] == target:
                line.positions.add((irow, i))
            else:
                line.before = False

            if line.after and (i := icolumn + k) < self._dim[0] and self._board[irow][i] == target:
                line.positions.add((irow, i))
            else:
                line.after = False

            # before (top) is not needed for vertical victory.
            line = lines['vertical']
            if line.after and (i := irow + k) < self._dim[1] and self._board[i][icolumn] == target:
                line.positions.add((i, icolumn))
            else:
                line.after = False

            line = lines['diagonal1']
            if line.before and (i := icolumn - k) >= 0 and (j := irow - k) >= 0 and self._board[j][i] == target:
                line.positions.add((j, i))
            else:
                line.before = False

            if line.after and (i := icolumn + k) < self._dim[0] and (j := irow + k) < self._dim[1] and self._board[j][i] == target:
                line.positions.add((j, i))
            else:
                line.after = False

            line = lines['diagonal2']
            if line.before and (i := icolumn - k) >= 0 and (j := irow + k) < self._dim[1] and self._board[j][i] == target:
                line.positions.add((j, i))
            else:
                line.before = False

            if line.after and (i := icolumn + k) < self._dim[0] and (j := irow - k) >= 0 and self._board[j][i] == target:
                line.positions.add((j, i))
            else:
                line.after = False

            if not any(check for check in lines.values()):
                break

        for line in lines.values():
            if len(line.positions) >= 4:
                self._win_points |= line.positions

    def _check_tie(self):
        return not any(case == Players.NONE for row in self._board for case in row)

    def reset(self) -> None:
        """
        Reset the game.
        """
        self._board = self.create_empty_board(self._dim)
        self.plays_history = []
        self._win_points = set()
        self.turn = Players.ONE
