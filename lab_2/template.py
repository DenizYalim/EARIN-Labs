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
            return

        someone_won = self._winning_move(self.board, self.current_player)
        is_draw = self._check_draw(board=self.board)

        if someone_won:
            print(f"Player {self.current_player} won!")
            self.game_over = True
            return
        elif is_draw:
            print("It's a draw!")
            self.game_over = True
            return

        self.current_player = self.__get_reverse_of_piece(self.current_player)

    def _place_piece(self, board, column, piece) -> tuple:
        column = int(column)

        if column < 0 or column >= COLS:
            print(f"Invalid column. Please enter a number between 0 and {COLS - 1}.")
            return False, None

        current_row = ROWS - 1
        while current_row >= 0:
            if board[current_row][column] == EMPTY:
                board[current_row][column] = piece
                return True, piece
            current_row -= 1

        if board == self.board:
            print("Column is full, try a different column.")
        return False, None

    def _winning_move(self, board, piece):
        for row in range(ROWS):
            for col in range(COLS - 3):
                if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece:
                    return True

        for row in range(ROWS - 3):
            for col in range(COLS):
                if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                    return True

        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece:
                    return True

        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                    return True

        return False

    def _check_draw(self, board):
        for spot in board[0]:
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

    def evaluate_position(self, board: list[list[str]], piece):
        opponent = self.__get_reverse_of_piece(piece)

        if self._winning_move(board, piece):
            return 1337
        if self._winning_move(board, opponent):
            return -1337

        positional_score = 0
        for row, board_row in enumerate(board):
            for col, cell in enumerate(board_row):
                piece_value = COLS // 2 - abs(COLS // 2 - col) + ROWS // 2 - abs(ROWS // 2 - row)

                if cell == piece:
                    positional_score += piece_value
                elif cell == opponent:
                    positional_score -= piece_value

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

        best_col, best_score = self.minimax(
            board=og_board,
            depth=depth,
            maximizing_player=True,
            alpha=float("-inf"),
            beta=float("inf"),
            ai_piece=piece,
        )

        return best_col, best_score

    def minimax(self, board, depth, maximizing_player, alpha, beta, ai_piece) -> tuple:
        opponent_piece = self.__get_reverse_of_piece(ai_piece)

        if depth == 0:
            return None, self.evaluate_position(board, ai_piece)

        valid_columns = [col for col in range(COLS) if board[0][col] == EMPTY]

        if maximizing_player:
            best_score = float("-inf")
            best_col = valid_columns[0] if valid_columns else None

            for col in valid_columns:
                temp_board = self._copy_board(board)
                success, _ = self._place_piece(board=temp_board, column=col, piece=ai_piece)

                if not success:
                    continue

                _, score = self.minimax(
                    board=temp_board,
                    depth=depth - 1,
                    maximizing_player=False,
                    alpha=alpha,
                    beta=beta,
                    ai_piece=ai_piece,
                )

                if score > best_score:
                    best_score = score
                    best_col = col

            return best_col, best_score

        else:
            best_score = float("inf")
            best_col = valid_columns[0] if valid_columns else None

            for col in valid_columns:
                temp_board = self._copy_board(board)
                success, _ = self._place_piece(board=temp_board, column=col, piece=opponent_piece)

                if not success:
                    continue

                _, score = self.minimax(
                    board=temp_board,
                    depth=depth - 1,
                    maximizing_player=True,
                    alpha=alpha,
                    beta=beta,
                    ai_piece=ai_piece,
                )

                if score < best_score:
                    best_score = score
                    best_col = col

            return best_col, best_score


def main():
    game = ConnectFour()

    player_preferences = input("Do you want to play as 'X' (goes first) or 'O' (goes second)? Enter X or O: ").strip().upper()
    while player_preferences not in [PLAYER_X, PLAYER_O]:
        print("Invalid input.")
        player_preferences = input("Do you want to play as 'X' (goes first) or 'O' (goes second)? Enter X or O: ").strip().upper()

    while True:
        if game.game_over:
            game.print_board()
            break

        if game.current_player == player_preferences:
            game.print_board()

            minmax_eval = game.get_move_from_minmax(piece=game.current_player)

            column_inputted = input(f"where to place piece? (0-{COLS - 1}) ; optimal minmax move to play: {minmax_eval[0]} with score: {minmax_eval[1]}\n")
            if not column_inputted.isdigit() or int(column_inputted) < 0 or int(column_inputted) >= COLS:
                print("\nInvalid input. Please enter a valid column number.")
                continue

        else:
            game.print_board()
            move, score = game.get_move_from_minmax(piece=game.current_player)
            print(f"AI plays column {move} with score {score}")
            column_inputted = move

        game.game_turn(int(column_inputted))


if __name__ == "__main__":
    main()
