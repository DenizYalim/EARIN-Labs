# ##### XO


class Board:
    map: list[list[chr]]  # can be #->empty, X or O
    first_players_turn: bool
    column_size: int
    row_size: int

    def __init__(self):
        self.first_players_turn = True
        self.column_size = 7
        self.row_size = 6

    def put_piece(self, column):
        piece = "X"
        if not self.first_players_turn:
            piece = "O"

        row = self.row_size
        while self.map[row][column] != "#":
            row += 1
        self.map[row][column] = piece
