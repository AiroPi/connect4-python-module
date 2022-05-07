from typing import Any, TypeAlias, List, Literal, Optional, Tuple, Sequence
from enum import Enum


Token: TypeAlias = str


class Players(Enum):
    ONE = 1
    TWO = 2


class Power4:
    def __init__(self, player1: Token = "x", player2: Token = "o", empty: Token = " ", dimensions: Sequence[int] = (7, 6)):
        self.player1: Token = player1
        self.player2: Token = player2
        self.empty: Token = empty
        self._dimensions: Tuple[int] = tuple(dimensions[::-1])
        self._dim = self._dimensions

        self._board: List[List[Literal[0, 1, 2]]] = [[0] * self._dim[1] for _ in range(self._dim[0])]
        self.turn: Players = Players.ONE

    @property
    def dimensions(self) -> Tuple[int]:
        return self._dimensions[::-1]

    @property
    def board(self) -> List[List[Literal[0, 1, 2]]]:
        return self._board

    @property
    def strboard(self) -> str:
        return ''.join(''.join((self.empty, self.player1, self.player2)[case] for case in row) + '\n' for row in self.board)

    def get_turn(self) -> Literal[1, 2]:
        return self.turn.value

    def play(self, column: int) -> bool:
        for row in self.board[::-1]:
            if row[column] == 0:
                row[column] = self.get_turn()
                break
        else:
            raise ValueError("Column full")

        if self.turn == Players.ONE:
            self.turn = Players.TWO
        else:
            self.turn = Players.ONE

        return self.get_win()

    def check_win(self) -> bool:
        return True

    def get_win(self) -> Optional[Tuple[Tuple]]:
        winner = 0
        winner_tokens = []
        for i in range(self._dim[0]):
            prev = 0
            chain = []
            for j in range(self._dim[1]):
                if self._board[i][j] == prev and self._board[i][j] != 0:
                    chain.append((i, j))
                else:
                    if len(chain) >= 4:
                        winner_tokens.extend(chain)
                        break
                    chain = [(i, j)]
                    prev = self._board[i][j]

        for j in range(self._dim[1]):
            prev = 0
            chain = []
            for i in range(self._dim[0]):
                if self._board[i][j] == prev and self._board[i][j] != 0:
                    chain.append((i, j))
                else:
                    if len(chain) >= 4:
                        winner_tokens.extend(chain)
                        break
                    chain = [(i, j)]
                    prev = self._board[i][j]

        for j in range(self._dim[1]):
            prev = 0
            chain = []
            for i in range(self._dim[0]):
                if self._board[i][j] == prev and self._board[i][j] != 0:
                    chain.append((i, j))
                else:
                    if len(chain) >= 4:
                        winner_tokens.extend(chain)
                        break
                    chain = [(i, j)]
                    prev = self._board[i][j]

        return winner_tokens


def main():
    power4 = Power4()
    power4.play(0)
    power4.play(0)
    power4.play(0)
    print(power4.play(0))
    print(power4.play(0))
    print(power4.play(1))
    print(power4.play(1))
    print(power4.play(1))
    print(power4.play(1))
    print(power4.strboard)


if __name__ == "__main__":
    main()
