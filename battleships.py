# import functions
from random import randint
from math import ceil

# some style stuff
markings_l = ">>>>>>>>>>>>>>>>>>>>"
markings_r = "<<<<<<<<<<<<<<<<<<<<"

# let the player choose the size of the board
n_rows = int(raw_input("Number of rows:"))
n_cols = int(raw_input("Number of columns:"))

# let the player choose the number of battleships
n_ships = 0
n_ships_max = int(ceil(n_rows * n_cols / 8))
while n_ships >= (n_ships_max + 1) or n_ships <= 0:
    n_ships = int(raw_input("Number of battleships (1 - %s):" % n_ships_max))

# calculate the number of turns
n_fields = n_rows * n_cols
n_turns = int(ceil(((float(n_ships) / float(n_fields - 1)) ** 0.5) * n_fields))

# generate the board
board = []
row_range = range(n_rows)
col_range = range(n_cols)

for x in row_range:
    board.append(["#"] * n_cols)
    
def print_board(board):
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~"
    for row in board:
        print " ".join(row)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~"

board_pc = []
for x in row_range:
    board_pc.append(["#"] * n_cols)

# generate the ships
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

    ship_space = [[-1, 0, 1, 1, 1, 0, -1, -1], [1, 1, 1, 0, -1, -1, -1, 0]]

    for i in range(8):
        ship_space[0][i] = ship_row + ship_space[0][i]
        ship_space[1][i] = ship_col + ship_space[1][i]

    for i in range(8):
        if (ship_space[0][i] in row_range) and (ship_space[1][i] in col_range):
            board_pc[ship_space[0][i]][ship_space[1][i]] = "%"

# define game-play objects and functions
turn = 0

ships_left = n_ships

def print_begin_game():
    print ""
    print markings_l,
    print "Let's play Battleship!",
    print markings_r
    print "You have %s turns." % (n_turns)
    print_board(board)

def print_turn():
    print ""
    print markings_l,
    print " Turn %s " % (turn + 1),
    print markings_r

def request_guess():
    global guess_row
    guess_row = -1
    global guess_col
    guess_col = -1
    while guess_row not in row_range:
        guess_row = int(raw_input("Guess Row (1 - %s):" % (n_rows))) - 1
    while guess_col not in col_range:
        guess_col = int(raw_input("Guess Col (1 - %s):" % (n_cols))) - 1

def check_last_ship():
    if ships_left > 0:
        print "You sunk one of my battleships!"
        board[guess_row][guess_col] = "X"
        board_pc[guess_row][guess_col] = "O"
    elif ships_left == 0:
        print "Congratulations! You sunk all of my battleships!"
        board[guess_row][guess_col] = "X"

def uncover_ship_space():
    ship_space = [[-1, 0, 1, 1, 1, 0, -1, -1], [1, 1, 1, 0, -1, -1, -1, 0]]
    for i in range(8):
        ship_space[0][i] = guess_row + ship_space[0][i]
        ship_space[1][i] = guess_col + ship_space[1][i]
    for i in range(8):
        if (ship_space[0][i] in row_range) and (ship_space[1][i] in col_range):
            global board
            board[ship_space[0][i]][ship_space[1][i]] = "O"

def check_hit_miss():
    if (board_pc[guess_row][guess_col] == "X"):
        global ships_left
        ships_left -= 1
        check_last_ship()
        uncover_ship_space()
        print_board(board)
    else:
        print "You missed my battleships!"
        board[guess_row][guess_col] = "O"
        print_board(board)

def check_guess_history():
    if (board[guess_row][guess_col] == "O") or (board[guess_row][guess_col] == "X"):
        print "You guessed that one already."
    else:
        global turn
        turn += 1
        check_hit_miss()

# game
print_begin_game()

    # loop through the turns
while turn < n_turns and ships_left > 0:
    print_turn()
    request_guess()
    check_guess_history()

    # game over?
if turn == n_turns and ships_left > 0:
    print ""
    print markings_l,
    print " GAME OVER ",
    print markings_r
    print_board(board_pc)
