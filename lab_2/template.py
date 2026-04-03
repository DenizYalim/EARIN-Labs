import copy

EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"
ROWS = 6
COLS = 7

MINMAX_DEPTH = 4


class ConnectFour:
    """
    Class for game Connect 4

    """

    def __init__(self):
        self.board = [[EMPTY] * COLS for _ in range(ROWS)]
        self.current_player = PLAYER_X
        self.game_over = False

    def game_turn(self, column) -> None:
        if self.game_over:
            print(f"Player {self.current_player} has already won!")
            return

        if not self._place_piece(board=self.board, column=column, piece=self.current_player):
            return  # invalid move, piece not placed

        someone_won = self._winning_move(self.board, self.current_player)
        is_draw = self._check_draw(board=self.board)

        if someone_won:
            print(f"Player {self.current_player} won!")
            self.game_over = True
            return
        elif is_draw:
            print("It's a draw!")
            self.game_over = True  # end the game on draw as well
            return

        self.current_player = self.__get_reverse_of_piece(self.current_player)

    def _place_piece(self, board, column, piece) -> bool:  # bool to show succesful placement
        column = int(column)  # typecast str to int, it will crash if given string

        if column < 0 or column >= COLS:
            print(f"Invalid column. Please enter a number between 0 and {COLS - 1}.")
            return False, None

        # piece = self.current_player

        current_row = ROWS - 1
        while current_row >= 0:
            if board[current_row][column] == EMPTY:
                board[current_row][column] = piece

                # switch player for next turn
                """if self.current_player == PLAYER_X:
                    self.current_player = PLAYER_O
                else:
                    self.current_player = PLAYER_X"""

                return True, piece
            current_row -= 1

        print("Column is full, try a different column.")
        return False, None

    def _winning_move(self, board, piece):
        # horizontal check
        for row in range(ROWS):
            for col in range(COLS - 3):
                if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece:
                    return True

        # vertical check
        for row in range(ROWS - 3):
            for col in range(COLS):
                if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                    return True

        # diagonal down-right check
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece:
                    return True

        # diagonal up-right check
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                    return True

        return False

    def _check_draw(self, board):  # if all top cells are filled and no winner, then it's a draw
        if self.game_over:
            return False

        for spot in board[0]:  # check top row
            if spot == EMPTY:
                return False

        return True

    def _copy_board(self, board=None):
        if board is None:
            board = self.board
        return copy.deepcopy(board)

    def print_board(self):
        print()
        for row in self.board:
            print("|".join(row))
        print("-" * (COLS * 2 - 1))
        print(" ".join(str(i) for i in range(COLS)))

    # Implement any additional functions needed here

    """def evaluate_window(self, window, piece):
        
        Evaluation of given window. Helper function to evaluate the separate parts of the board called windows

        Parameters:
        - window: list containing values of evaluated window
        - piece: PLAYER_X or PLAYER_O depending on which player's position we evaluate

        Returns:
        - score of the window

        """

    def get_move_from_minmax(self, piece, og_board=None, depth=MINMAX_DEPTH, alpha=0, beta=0) -> tuple:
        if og_board is None:
            og_board = self.board  # since def args can't access object itself, this is the work around

        if depth == 0:
            # might be a good idea to seperate this to two functions; as currently we have 2 different return outputs. this line should only be called internally.
            return self.evaluate_position(og_board, piece)

        move_list = []  # list of tuples: (move, score)
        for col in range(COLS):
            temp_board = self._copy_board(og_board)
            self._place_piece(board=temp_board, column=col, piece=piece)

            score = self.get_move_from_minmax(og_board=temp_board, piece=self.__get_reverse_of_piece(piece), depth=depth - 1, alpha=alpha, beta=beta)

            move_list.append((col, score))

        move_list.sort(key=lambda x: x[1], reverse=True)
        return move_list[0]  # return column with best score"""

    def evaluate_position(self, board, piece):
        """
        Evaluation of position
        Parameters:
        - board: 2d matrix representing evaluated state of the board
        - piece: PLAYER_X or PLAYER_O depending on which player's position we evaluate

        Returns:
        - score of the position

        """
        # default states = already_won, already_tied, already_lost
        if self._winning_move(board, piece):
            return 1337
        if self._winning_move(board, self.__get_reverse_of_piece(piece)):
            return -1337

        return 0

    def __get_reverse_of_piece(self, piece) -> str:
        if piece == PLAYER_O:
            return PLAYER_X

        if piece == PLAYER_X:
            return PLAYER_O

        raise ValueError(f"Invalid piece {piece} given, expected {PLAYER_X} or {PLAYER_O}")

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        """
        Minimax with alpha-beta pruning algorithm

        Parameters:
        - board: 2d matrix representing the state, each cell contains either ' ' (empty cell), 'X' (player1), or 'O' (player2)
        - depth: depth
        - maximizing_player: boolean which is equal to True when the player tries to maximize the score
        - alpha: alpha variable for pruning
        - beta: beta variable for pruning

        Returns:
        - Best value
        - Best move found

        """

        # Your code starts here


def main():
    """
    Main game loop implementation. Player1 should play first with 'X', player2 plays second with 'O'
    """
    game = ConnectFour()

    while True:
        game.print_board()
        minmax_eval = game.get_move_from_minmax(piece=game.current_player)[0]
        print(f"output: {minmax_eval}")
        column_inputted = input(f"where to place piece? (0-6); optimal minmax move to play: {minmax_eval[0]} with score: {minmax_eval[1]}  \n")
        game.game_turn(column_inputted)


if __name__ == "__main__":
    main()
