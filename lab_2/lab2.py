import math
import random

ROWS = 6
COLS = 7
PLAYER = "X"
AI = "O"
EMPTY = " "

DEPTH = 4

def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("\n")
    for r in range(ROWS):
        print("|" + "|".join(board[r]) + "|")
    print("---------------")
    print(" 1 2 3 4 5 6 7")

def manual_copy(board):
    return [row[:] for row in board]

def drop_piece(board, col, piece):
    if board[0][col] != EMPTY:
        return False
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = piece
            return True
    return False

def check_win(b, p):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(b[r][c+i] == p for i in range(4)):
                return True

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(b[r+i][c] == p for i in range(4)):
                return True

    # Positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(b[r+i][c+i] == p for i in range(4)):
                return True

    # Negative diagonal
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(b[r-i][c+i] == p for i in range(4)):
                return True

    return False

def get_valid_moves(board):
    return [c for c in range(COLS) if board[0][c] == EMPTY]

# SIMPLE EVALUATION FUNCTION
def evaluate_window(window, piece):
    score = 0
    opponent = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def evaluate_position(board, piece):
    score = 0

    # Center column prfc
    center_col = [board[r][COLS // 2] for r in range(ROWS)]
    score += center_col.count(piece) * 3

    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = [board[r][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = [board[r+i][c] for i in range(4)]
            score += evaluate_window(window, piece)

    # Diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def is_terminal(board):
    return check_win(board, PLAYER) or check_win(board, AI) or len(get_valid_moves(board)) == 0

# MINIMAX WITH ALPHA-BETA
def minimax(board, depth, alpha, beta, maximizing):
    valid_moves = get_valid_moves(board)
    terminal = is_terminal(board)

    if depth == 0 or terminal:
        if terminal:
            if check_win(board, AI):
                return (None, 100000)
            elif check_win(board, PLAYER):
                return (None, -100000)
            else:
                return (None, 0)
        else:
            return (None, evaluate_position(board, AI))

    if maximizing:
        value = -math.inf
        best_col = random.choice(valid_moves)

        for col in valid_moves:
            temp = manual_copy(board)
            drop_piece(temp, col, AI)
            new_score = minimax(temp, depth-1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_moves)

        for col in valid_moves:
            temp = manual_copy(board)
            drop_piece(temp, col, PLAYER)
            new_score = minimax(temp, depth-1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break

        return best_col, value

# Main Game
game_board = create_board()
print("Connect 4 - AI Project")

user_input = input("Choose turn: 1 to go first, 2 to go second: ")
current_turn = PLAYER if user_input == "1" else AI

while True:
    print_board(game_board)

    if current_turn == PLAYER:
        try:
            player_move = int(input("Enter column (1-7): ")) - 1
            if 0 <= player_move < COLS:
                if drop_piece(game_board, player_move, PLAYER):
                    if check_win(game_board, PLAYER):
                        print_board(game_board)
                        print("Congratulations! Player wins.")
                        break
                    current_turn = AI
                else:
                    print("Column full! Try again.")
            else:
                print("Out of range!")
        except ValueError:
            print("Invalid input.")

    else:
        print("AI is calculating")
        col, _ = minimax(game_board, DEPTH, -math.inf, math.inf, True)
        drop_piece(game_board, col, AI)

        if check_win(game_board, AI):
            print_board(game_board)
            print("Game Over, AI has won.")
            break

        current_turn = PLAYER

    if len(get_valid_moves(game_board)) == 0:
        print_board(game_board)
        print("It's a draw!")
        break
