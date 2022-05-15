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

        self.plays_history.append((column, self._idim[1] - i))
        self.get_win(column, self._idim[1] - i)

        if self.turn == Players.ONE:
            self.turn = Players.TWO
        else:
            self.turn = Players.ONE

        return self._win_points

    def get_win(self, icolumn, irow):
        target = self.get_turn()
        print(target)

        lines = {
            'horizontal': [{(irow, icolumn)}, True, True],
            'vertical': [{(irow, icolumn)}, True, True],
            'diagonal1': [{(irow, icolumn)}, True, True],
            'diagonal2': [{(irow, icolumn)}, True, True]
        }

        for k in range(1, max(self._dim[0], self._dim[1])):
            line = lines['horizontal']
            if line[1] and (i := icolumn - k) >= 0 and self._board[irow][i] == target:
                line[0].add((irow, i))
            else:
                print()
                line[1] = False

            if line[2] and (i := icolumn + k) < self._dim[0] and self._board[irow][i] == target:
                line[0].add((irow, i))
            else:
                line[2] = False

            line = lines['vertical']
            if line[1] and (i := irow - k) >= 0 and self._board[i][icolumn] == target:
                line[0].add((i, icolumn))
            else:
                line[1] = False

            if line[2] and (i := irow + k) < self._dim[1] and self._board[i][icolumn] == target:
                line[0].add((i, icolumn))
            else:
                line[2] = False

            line = lines['diagonal1']
            if line[1] and (i := icolumn - k) >= 0 and (j := irow - k) >= 0 and self._board[j][i] == target:
                line[0].add((j, i))
            else:
                line[1] = False

            if line[2] and (i := icolumn + k) < self._dim[0] and (j := irow + k) < self._dim[1] and self._board[j][i] == target:
                line[0].add((j, i))
            else:
                line[2] = False

            line = lines['diagonal2']
            if line[1] and (i := icolumn - k) >= 0 and (j := irow + k) < self._dim[1] and self._board[j][i] == target:
                line[0].add((j, i))
            else:
                line[1] = False

            if line[2] and (i := icolumn + k) < self._dim[0] and (j := irow - k) >= 0 and self._board[j][i] == target:
                line[0].add((j, i))
            else:
                line[2] = False

            if not any(check for info in lines.values() for check in info[1:]):
                break


        for line in lines.values():
            if len(line[0]) >= 4:
                self._win_points = line[0]

    def show_history(self):
        board = self.create_empty_board(self._dim)
        for i, (column, row) in enumerate(self.plays_history):
            board[row][column] = i + 1

        return board


def main():
    power4 = Connect4()
    while True:
        print(''.join(map(str, range(7))))
        print(power4.strboard(empty="."))
        play = input("Player {} turn: ".format(power4.get_turn()))
        result = power4.play(int(play))

        if result:
            print("gg u win")
            break
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
