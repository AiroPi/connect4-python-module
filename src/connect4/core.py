from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal, Sequence, TypeAlias, cast

from connect4.errors import ColumnFull, GameOver, InvalidColumn

Token: TypeAlias = str


class Players(Enum):
    ONE = 1
    TWO = 2


class Connect4:
    def __init__(self, dimensions: Sequence[int] = (7, 6)):
        self._dimensions: tuple[int, int] = (dimensions[0], dimensions[1])
        self._idim: tuple[int, int] = (self._dimensions[0] - 1, self._dimensions[1] - 1)
        self.plays_history: list[tuple[int, int]] = []
        self._win_points: set[tuple[int, int]] = set()

        self._board: list[list[Literal[0, 1, 2]]] = self.create_empty_board(self._dimensions)
        self.turn: Players = Players.ONE

        self._dim = self._dimensions

    @property
    def dimensions(self) -> tuple[int, int]:
        return self._dimensions

    @property
    def yxboard(self) -> list[list[Literal[0, 1, 2]]]:
        return [[row[i] for row in self._board] for i in range(self._dim[1])[::-1]]

    @property
    def board(self):
        return self._board

    @staticmethod
    def create_empty_board(dimensions: Sequence[int]) -> list[list[Any]]:
        return [[0] * dimensions[0] for _ in range(dimensions[1])]

    def strboard(self, player1: Token = "x", player2: Token = "o", win_player1: Token = "X", win_player2: Token = "O", empty: Token = " ") -> str:
        board: list[list[int]] = cast(list[list[int]], self.board.copy())
        for row, column in self._win_points:
            board[row][column] = 3 if self._board[row][column] == Players.ONE.value else 4
        return ''.join(''.join((empty, player1, player2, win_player1, win_player2)[case] for case in row) + '\n' for row in self.board)[:-1]

    def get_turn(self) -> Literal[1, 2]:
        return self.turn.value

    def play(self, column: int):
        if self._win_points:
            raise GameOver(self.get_turn())

        if column < 0 or column >= self._dim[0]:
            raise InvalidColumn(column)

        for i, row in enumerate(self._board[::-1]):
            if row[column] == 0:
                row[column] = self.get_turn()
                break
        else:
            raise ColumnFull(column)

        self.plays_history.append((column, self._idim[1] - i))
        self.get_win(column, self._idim[1] - i)

        if not self._win_points:
            if self.turn == Players.ONE:
                self.turn = Players.TWO
            else:
                self.turn = Players.ONE

        return self._win_points

    def get_win(self, icolumn, irow):
        target = self.get_turn()

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
                self._win_points = line.positions

    def show_history(self):
        board = self.create_empty_board(self._dim)
        for i, (column, row) in enumerate(self.plays_history):
            board[row][column] = i + 1

        return board
