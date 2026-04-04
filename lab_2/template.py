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

        if not self._place_piece(board=self.board, column=column, piece=self.current_player)[0]:
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

    def _place_piece(self, board, column, piece) -> tuple:  # tuple of (success, piece)
        column = int(column)  # typecast str to int, it will crash if given string

        if column < 0 or column >= COLS:
            print(f"Invalid column. Please enter a number between 0 and {COLS - 1}.")
            return False, None

        # piece = self.current_player

        current_row = ROWS - 1
        while current_row >= 0:
            if board[current_row][column] == EMPTY:
                board[current_row][column] = piece

                return True, piece
            current_row -= 1

        if board == self.board:  # don't print if its a simulation
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

    def evaluate_position(self, board: list[list[str]], piece):
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

        # pieces on the middle should be more valuable,
        positional_score = 0
        for row, list in enumerate(board):
            for col, cell in enumerate(list):
                piece_value = COLS // 2 - abs(COLS // 2 - col) + ROWS // 2 - abs(ROWS // 2 - row)  # pieces in the middle are more valuable
                if cell == piece:  # our piece
                    positional_score += piece_value
                elif cell == self.__get_reverse_of_piece(piece):  # opponent piece
                    positional_score -= piece_value
                else:
                    pass  # empty cell

        return positional_score

    def __get_reverse_of_piece(self, piece) -> str:
        if piece == PLAYER_O:
            return PLAYER_X

        if piece == PLAYER_X:
            return PLAYER_O

        raise ValueError(f"Invalid piece {piece} given, expected {PLAYER_X} or {PLAYER_O}")

    def get_move_from_minmax(self, piece, og_board=None, depth=MINMAX_DEPTH) -> tuple:
        if og_board is None:
            og_board = self.board

        if depth == 0:
            return (-1, self.evaluate_position(og_board, piece))

        move_list = []

        for col in range(COLS):
            temp_board = self._copy_board(og_board)
            success, _ = self._place_piece(board=temp_board, column=col, piece=piece)

            if not success:
                continue

            _, score = self.get_move_from_minmax(piece=self.__get_reverse_of_piece(piece), og_board=temp_board, depth=depth - 1)

            move_list.append((col, score))

        if not move_list:
            return (-1, self.evaluate_position(og_board, piece))

        move_list.sort(key=lambda x: x[1], reverse=True)
        return move_list[0]

    def minimax(self, board, depth, maximizing_player, alpha, beta) -> tuple:  # value, column of best move
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

    player_preferences = input("Do you want to play as 'X' (goes first) or 'O' (goes second)? Enter X or O: ").strip().upper()
    while player_preferences not in [PLAYER_X, PLAYER_O]:
        print("Invalid input. Defaulting to 'X'.")
        player_preferences = input("Do you want to play as 'X' (goes first) or 'O' (goes second)? Enter X or O: ").strip().upper()

    while True:
        game.print_board()
        minmax_eval = game.get_move_from_minmax(piece=game.current_player)
        print(f"output: {minmax_eval}")
        column_inputted = input(f"where to place piece? (0-{COLS - 1}); optimal minmax move to play: {minmax_eval[0]} with score: {minmax_eval[1]}  \n")
        if not column_inputted.isdigit() or int(column_inputted) < 0 or int(column_inputted) >= COLS:
            print("\nInvalid input. Please enter a valid column number.")
            continue
        game.game_turn(int(column_inputted))


if __name__ == "__main__":
    main()
