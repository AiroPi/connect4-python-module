class GameOver(Exception):
    def __init__(self, winner):
        super().__init__(f"Game is over, winner is player {winner}")
        self.winner = winner


class ColumnFull(Exception):
    def __init__(self, column_index):
        super().__init__(f"The column {column_index} is full")
        self.column_index = column_index


class InvalidColumn(Exception):
    def __init__(self, column_index) -> None:
        super().__init__(f"The column {column_index} is out of range.")
        self.column_index = column_index
