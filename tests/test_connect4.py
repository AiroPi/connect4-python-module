from pprint import pprint

import connect4
import pytest


def test_init():
    c4 = connect4.Connect4(dimensions=(4, 4))
    assert c4.board == [[0] * 4 for i in range(4)]
    assert c4.strboard() == ((' ' * 4 + '\n') * 4)[:-1]


def test_vertical_victory():
    c4 = connect4.Connect4()
    assert c4.play(0) == set()
    assert c4.play(1) == set()
    assert c4.play(0) == set()
    assert c4.play(1) == set()
    assert c4.play(0) == set()
    assert c4.play(1) == set()
    assert c4.play(0) == {(5, 0), (4, 0), (3, 0), (2, 0)}

    with pytest.raises(connect4.GameOver) as exception:
        c4.play(1)

    assert exception.value.winner == 1


def test_horizontal_victory():
    c4 = connect4.Connect4()
    c4.play(0)
    c4.play(0)
    c4.play(1)
    c4.play(1)
    c4.play(2)
    c4.play(2)
    assert c4.play(3) == {(5, 0), (5, 1), (5, 2), (5, 3)}

    with pytest.raises(connect4.GameOver) as exception:
        c4.play(1)

    assert exception.value.winner == 1


def test_diagonal1_victory():
    c4 = connect4.Connect4()
    c4.play(0)
    c4.play(1)
    c4.play(1)
    c4.play(2)
    c4.play(2)
    c4.play(6)
    c4.play(2)
    c4.play(3)
    c4.play(3)
    c4.play(3)
    assert c4.play(3) == {(2, 3), (3, 2), (4, 1), (5, 0)}

    with pytest.raises(connect4.GameOver) as exception:
        c4.play(3)

    assert exception.value.winner == 1


def test_diagonal2_victory():
    c4 = connect4.Connect4()
    c4.play(5)
    c4.play(6)
    c4.play(4)
    c4.play(5)
    c4.play(4)
    c4.play(4)
    c4.play(3)
    c4.play(3)
    c4.play(3)
    assert c4.play(3) == {(5, 6), (4, 5), (3, 4), (2, 3)}

    with pytest.raises(connect4.GameOver) as exception:
        c4.play(3)

    assert exception.value.winner == 2
