from operator import sub
from typing import TypeAlias, Literal, Optional, Sequence
from enum import Enum
from pprint import pprint


Token: TypeAlias = str


class Players(Enum):
    ONE = 1
    TWO = 2


class Connect4:
    def __init__(self, dimensions: Sequence[int] = (7, 6)):
        self._dimensions: tuple[int] = tuple(dimensions)
        self._dim = self._dimensions
        self._idim = tuple(map(sub, self._dim, (1, 1))) # idim = dimensions - 1 (indexed)
        self.plays_history = []
        self._win_points = set()

        self._board: list[list[Literal[0, 1, 2]]] = self.create_empty_board(self._dim)
        self.turn: Players = Players.ONE

    @property
    def dimensions(self) -> tuple[int]:
        return self._dimensions

    @property
    def yxboard(self) -> list[list[Literal[0, 1, 2]]]:
        return [[row[i] for row in self._board] for i in range(self._dim[1])[::-1]]

    @property
    def board(self):
        return self._board

    @staticmethod
    def create_empty_board(dimensions: Sequence[int]) -> list[list[Literal[0]]]:
        return [[0] * dimensions[0] for _ in range(dimensions[1])]


    def strboard(self, player1: Token = "x", player2: Token = "o", win_player1: Token = "X", win_player2: Token = "O", empty: Token = " ") -> str:
        board = self.board.copy()
        for row, column in self._win_points:
            board[row][column] = 3 if self._board[row][column] == Players.ONE.value else 4
        return ''.join(''.join((empty, player1, player2, win_player1, win_player2)[case] for case in row) + '\n' for row in self.board)[:-1]

    def get_turn(self) -> Literal[1, 2]:
        return self.turn.value

    def play(self, column: int):
        if self._win_points:
            raise Exception("Game is over")

        for i, row in enumerate(self._board[::-1]):
            if row[column] == 0:
                row[column] = self.get_turn()
                break
        else:
            raise ValueError("Column full")

        if self.turn == Players.ONE:
            self.turn = Players.TWO
        else:
            self.turn = Players.ONE

        self.plays_history.append((column, self._idim[1] - i))
        self.get_win(column, self._idim[1] - i)

        return self._win_points

    @staticmethod
    def inspect_line(line, pos):
        print(line, pos)
        target = line[pos]
        start = pos
        while (tmp := start - 1) >= 0 and line[tmp] == target:
            start = tmp

        end = pos
        while (tmp := end + 1) < len(line) and line[tmp] == target:
            end = tmp

        return start, end

    def find_win(self, line, pos):
        if abs(sub(*(tmp := self.inspect_line(line, pos)))) >= 3:
            for i in range(tmp[0], tmp[1] + 1):
                yield i

    def get_win(self, icolumn, irow):
        # horizontal check
        line = self._board[irow]
        for i in self.find_win(line, icolumn):
            self._win_points.add((irow, i))

        # vertical check
        line = [row[icolumn] for row in self._board]
        for i in self.find_win(line, irow):
            self._win_points.add((i, icolumn))

        # ascending check
        if icolumn >= (dif := abs(irow - self._idim[1])):
            tmp = icolumn - dif
            m = min(self._dim[1] - tmp + 1, self._idim[0])
            u, p = tmp, self._idim[1]
        else:
            tmp = icolumn + irow
            m = min(tmp + 1, self._idim[1])
            u, p = 0, tmp

        line = [self._board[p - i][u + i] for i in range(m)]
        for i in self.find_win(line, min(icolumn, self._idim[1] - irow)):
            self._win_points.add((p - i, u + i))

        # descending check
        # hm I'm lazy

    def show_history(self):
        board = self.create_empty_board(self._dim)
        for i, (column, row) in enumerate(self.plays_history):
            board[row][column] = i + 1

        return board


def main():
    power4 = Connect4()
    plays = [1, 5, 1, 1, 2, 2, 2, 5, 3, 5, 3, 6, 3, 6, 3, 6, 0]
    for i in plays:
        if power4.play(i):
            break
    print(power4.strboard())
    # print(row[slice(*power4.inspect_row(row, 2))])
    # print(power4._board)
    # power4.play(0)
    # power4.play(0)
    # power4.play(0)
    # print(power4.play(0))
    # print(power4.play(0))
    # print(power4.play(1))
    # print(power4.play(1))
    # print(power4.play(1))
    # print(power4.play(1))
    # print(power4.strboard())


if __name__ == "__main__":
    main()
