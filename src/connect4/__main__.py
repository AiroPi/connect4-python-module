from connect4 import Connect4

power4 = Connect4()
while True:
    print(''.join(map(str, range(7))))
    print(power4.strboard(empty="."))
    play = input("Player {} turn: ".format(power4.get_turn()))
    result = power4.play(int(play))

    if result:
        print(power4.strboard(empty="."))
        print("gg u win")
        break
