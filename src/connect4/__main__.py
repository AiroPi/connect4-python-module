from connect4 import Connect4, Players

c4 = Connect4()
while True:
    print(''.join(map(str, range(c4.dimensions[0]))))
    print(c4.strboard(empty="."))
    play = input(f"Player {c4.turn.value} turn: ")
    result = c4.play(int(play))

    if result or c4.turn == Players.NONE:
        print(c4.strboard(empty="."))
        print(f"Player {c4.turn.value} wins!" if result else "Tie!")
        break
