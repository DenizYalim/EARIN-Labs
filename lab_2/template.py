import copy

EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"
ROWS = 6
COLS = 7


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

        if not self._place_piece(column):
            return  # invalid move, piece not placed

        someone_won = self._winning_move(self.current_player)  # this is probably backwards, place_piece switches player and we check the opposite player here probably
        is_draw = self._check_draw()

        if someone_won:
            print(f"Player {self.current_player} won!")
            self.game_over = True
            return
        elif is_draw:
            print("It's a draw!")
            self.game_over = True  # end the game on draw as well
            return

        if self.current_player == PLAYER_X:  # reverse current_player for next turn
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X

    def _place_piece(self, column) -> bool:  # bool to show succesful placement
        column = int(column[0])  # typecast str to int, it will crash if given string

        if column < 0 or column >= COLS:
            print(f"Invalid column. Please enter a number between 0 and {COLS - 1}.")
            return False, None

        piece = self.current_player

        current_row = ROWS - 1
        while current_row >= 0:
            if self.board[current_row][column] == EMPTY:
                self.board[current_row][column] = piece

                # switch player for next turn
                """if self.current_player == PLAYER_X:
                    self.current_player = PLAYER_O
                else:
                    self.current_player = PLAYER_X"""

                return True, piece
            current_row -= 1

        print("Column is full, try a different column.")
        return False, None

    def _winning_move(self, piece):
        # horizontal check
        for row in range(ROWS):
            for col in range(COLS - 3):
                if self.board[row][col] == piece and self.board[row][col + 1] == piece and self.board[row][col + 2] == piece and self.board[row][col + 3] == piece:
                    return True

        # vertical check
        for row in range(ROWS - 3):
            for col in range(COLS):
                if self.board[row][col] == piece and self.board[row + 1][col] == piece and self.board[row + 2][col] == piece and self.board[row + 3][col] == piece:
                    return True

        # diagonal down-right check
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if self.board[row][col] == piece and self.board[row + 1][col + 1] == piece and self.board[row + 2][col + 2] == piece and self.board[row + 3][col + 3] == piece:
                    return True

        # diagonal up-right check
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if self.board[row][col] == piece and self.board[row - 1][col + 1] == piece and self.board[row - 2][col + 2] == piece and self.board[row - 3][col + 3] == piece:
                    return True

        return False

    def _check_draw(self):  # if all top cells are filled and no winner, then it's a draw
        if self.game_over:
            return False

        for spot in self.board[0]:  # check top row
            if spot == EMPTY:
                return False

        return True

    def print_board(self):
        print()
        for row in self.board:
            print("|".join(row))
        print("-" * (COLS * 2 - 1))
        print(" ".join(str(i) for i in range(COLS)))

    # Implement any additional functions needed here

    def evaluate_window(self, window, piece):
        """
        Evaluation of given window. Helper function to evaluate the separate parts of the board called windows

        Parameters:
        - window: list containing values of evaluated window
        - piece: PLAYER_X or PLAYER_O depending on which player's position we evaluate

        Returns:
        - score of the window

        """

    def evaluate_position(self, board, piece):
        """
        Evaluation of position
        Parameters:
        - board: 2d matrix representing evaluated state of the board
        - piece: PLAYER_X or PLAYER_O depending on which player's position we evaluate

        Returns:
        - score of the position

        """

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
        column_inputted = input("where to place piece? (0-6) ")
        game.game_turn(column_inputted)


if __name__ == "__main__":
    main()
