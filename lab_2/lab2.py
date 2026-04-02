import math

ROWS = 6
COLS = 7
PLAYER = "X"
AI = "O"
EMPTY = " "

def create_board():
    new_board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(EMPTY)
        new_board.append(row)
    return new_board

def print_board(board):
    print("\n")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += board[r][c] + "|"
        print(row_str)
    print("---------------")
    print(" 1 2 3 4 5 6 7")

def manual_copy(board):
    new_copy = []
    for r in range(ROWS):
        new_row = []
        for c in range(COLS):
            new_row.append(board[r][c])
        new_copy.append(new_row)
    return new_copy

def drop_piece(board, col, piece):
    if board[0][col] != EMPTY:
        return False
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = piece
            return True
    return False

def check_win(b, p):
    # Checks for every win condition which is possible
    # 1. Checks horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if b[r][c] == p and b[r][c+1] == p and b[r][c+2] == p and b[r][c+3] == p:
                return True
                
    # 2. Checks vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if b[r][c] == p and b[r+1][c] == p and b[r+2][c] == p and b[r+3][c] == p:
                return True
                
    # 3. Checks for positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if b[r][c] == p and b[r+1][c+1] == p and b[r+2][c+2] == p and b[r+3][c+3] == p:
                return True
                
    # 4. Checks for negative diagonal
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if b[r][c] == p and b[r-1][c+1] == p and b[r-2][c+2] == p and b[r-3][c+3] == p:
                return True
    return False

def get_ai_move(board):
    valid_cols = []
    for c in range(COLS):
        if board[0][c] == EMPTY:
            valid_cols.append(c)

    for col in valid_cols:
        temp = manual_copy(board)
        drop_piece(temp, col, AI)
        if check_win(temp, AI):
            return col

    for col in valid_cols:
        temp = manual_copy(board)
        drop_piece(temp, col, PLAYER)
        if check_win(temp, PLAYER):
            return col

    center_priority = [3, 2, 4, 1, 5, 0, 6]
    for col in center_priority:
        if col in valid_cols:
            return col
    return valid_cols[0]

# --- Main Game Execution ---
game_board = create_board()
print("Connect 4 - AI Project")
user_input = input("Choose turn: 1 to go first, 2 to go second: ")

if user_input == "1":
    current_turn = PLAYER
else:
    current_turn = AI

while True:
    print_board(game_board)
    
    if current_turn == PLAYER:
        try:
            player_move = int(input("Enter column (1-7): ")) - 1
            if player_move >= 0 and player_move < COLS:
                success = drop_piece(game_board, player_move, PLAYER)
                if success:
                    if check_win(game_board, PLAYER):
                        print_board(game_board)
                        print("Congratulations! Player wins.")
                        break
                    current_turn = AI
                else:
                    print("Column full! Try again.")
            else:
                print("Out of range! Pick 1-7.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    else:
        
        print("AI is calculating")
        ai_col = get_ai_move(game_board)
        drop_piece(game_board, ai_col, AI)
        if check_win(game_board, AI):
            print_board(game_board)
            print("Game Over, AI has won.")
            break
        current_turn = PLAYER

    is_full = True
    for c in range(COLS):
        if game_board[0][c] == EMPTY:
            is_full = False
    if is_full:
        print_board(game_board)
        print("It's a draw")
        break
