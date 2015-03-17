# import functions
from random import randint
from math import ceil

# some style stuff
markings_l = ">>>>>>>>>>>>>>>>>>>>"
markings_r = "<<<<<<<<<<<<<<<<<<<<"

# let the player choose the size of the board
n_rows = -1
while n_rows < 3 or n_rows > 10:
    n_rows = int(input("\nHow big do you want the square board to be? \nChoose the number of rows (3 - 10):"))
n_cols = n_rows

# calculate the number of battleships
n_ships = ceil(n_rows * n_cols / 8)

# calculate the number of turns
n_fields = n_rows * n_cols
n_turns = ceil(((n_ships / (n_fields - 1)) ** 0.5) * n_fields * (10 + n_rows) / 10)

# generate the board
board = []
row_range = range(n_rows)
col_range = range(n_cols)

for x in row_range:
    board.append(["#"] * n_cols)
    
def print_board(board):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for row in board:
        print(" ".join(row))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

board_pc = []
for x in row_range:
    board_pc.append(["#"] * n_cols)

# define game-play objects and functions

def ship_spacing(board, row, col, string):
    ship_space = [[-1, 0, 1, 1, 1, 0, -1, -1], [1, 1, 1, 0, -1, -1, -1, 0]]
    for i in range(8):
        ship_space[0][i] = row + ship_space[0][i]
        ship_space[1][i] = col + ship_space[1][i]
    for i in range(8):
        if (ship_space[0][i] in row_range) and (ship_space[1][i] in col_range):
            board[ship_space[0][i]][ship_space[1][i]] = string

    # generate the ships
def place_ships_on_board():
    global row_range, col_range, board_pc
    def random_row(board_range):
        return randint(0, len(row_range) - 1)
    def random_col(board_range):
        return randint(0, len(col_range) - 1)
    for ship in range(n_ships):
        ship_row = random_row(row_range)
        ship_col = random_col(col_range)
        while board_pc[ship_row][ship_col] == "X" or board_pc[ship_row][ship_col] == "%":
            ship_row = random_row(row_range)
            ship_col = random_col(col_range)
        board_pc[ship_row][ship_col] = "X"
        ship_spacing(board_pc, ship_row, ship_col, "%")

turn = 0

ships_left = n_ships

def print_begin_game():
    print("")
    print(markings_l, "Let's play Battleship!", markings_r)
    print("You have %s turns." % (n_turns))
    print("There are %s ships." % (n_ships))
    print_board(board)

def print_turn():
    if turn + 1 == n_turns:
        is_last = "(Last!) "
    else:
        is_last = ""
    print("\n")
    print(markings_l, " Turn %s " % (turn + 1), is_last, markings_r)

def request_guess():
    global guess_row
    guess_row = -1
    global guess_col
    guess_col = -1
    while guess_row not in row_range:
        guess_row = int(input("Guess Row (1 - %s):" % (n_rows))) - 1
    while guess_col not in col_range:
        guess_col = int(input("Guess Col (1 - %s):" % (n_cols))) - 1

def check_last_ship():
    if ships_left > 0:
        print("\nYou sunk one of my battleships!")
        board[guess_row][guess_col] = "X"
        board_pc[guess_row][guess_col] = "O"
    elif ships_left == 0:
        print("\nCongratulations! You sunk all of my battleships!")
        board[guess_row][guess_col] = "X"

def check_hit_miss():
    if (board_pc[guess_row][guess_col] == "X"):
        global ships_left
        ships_left -= 1
        check_last_ship()
        # Uncover ship space
        ship_spacing(board, guess_row, guess_col, "O")
        print_board(board)
    else:
        print("\nYou missed my battleships!")
        board[guess_row][guess_col] = "O"
        print_board(board)

def check_guess_history():
    if (board[guess_row][guess_col] == "O") or (board[guess_row][guess_col] == "X"):
        print("\nYou guessed that one already.")
    else:
        global turn
        turn += 1
        check_hit_miss()

############################## GAME EXECUTION #################################
place_ships_on_board()

print_begin_game()

    # loop through the turns
while turn < n_turns and ships_left > 0:
    print_turn()
    request_guess()
    check_guess_history()

    # game over?
if turn == n_turns and ships_left > 0:
    print("")
    print(markings_l, " GAME OVER ", markings_r)
    print_board(board_pc)
